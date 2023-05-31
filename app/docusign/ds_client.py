import uuid
from os import path


import requests
from flask import current_app as app, url_for, redirect, render_template, request, session
from flask_oauthlib.client import OAuth
from docusign_esign import ApiClient
from docusign_esign.client.api_exception import ApiException

from ..ds_config import DS_CONFIG, DS_JWT
from ..error_handlers import process_error
from ..jwt_helpers import get_jwt_token, get_private_key
from ..consts import API_TYPE

SCOPES = [
    "signature"
]

ROOMS_SCOPES = [
    "room_forms", "dtr.rooms.read", "dtr.rooms.write",
    "dtr.documents.read", "dtr.documents.write", "dtr.profile.read",
    "dtr.profile.write", "dtr.company.read", "dtr.company.write"
]

CLICK_SCOPES = [
    "signature", "click.manage", "click.send"
]

ADMIN_SCOPES = [
    "signature", "organization_read", "group_read", "permission_read", "user_read", "user_write", 
    "account_read", "domain_read", "identity_provider_read", "impersonation", "user_data_redact"
]


class DSClient:
    ds_app = None

    @classmethod
    def _init(cls, auth_type, api):
        if auth_type == "code_grant":
            cls._auth_code_grant(api)
        elif auth_type == "jwt":
            cls._jwt_auth(api)

    @classmethod
    def _auth_code_grant(cls, api):
        """Authorize with the Authorization Code Grant - OAuth 2.0 flow"""
        oauth = OAuth(app)

        use_scopes = []

        if api == "Rooms":
            use_scopes.extend(ROOMS_SCOPES)
        elif api == "Click":
            use_scopes.extend(CLICK_SCOPES)
        elif api == "Admin":
            use_scopes.extend(ADMIN_SCOPES)
        else:
            use_scopes.extend(SCOPES)
        # remove duplicate scopes
        use_scopes = list(set(use_scopes))
        
        request_token_params = {
            "scope": " ".join(use_scopes),
            "state": lambda: uuid.uuid4().hex.upper()
        }
        if not DS_CONFIG["allow_silent_authentication"]:
            request_token_params["prompt"] = "login"
        cls.ds_app = oauth.remote_app(
            "docusign",
            consumer_key=DS_CONFIG["ds_client_id"],
            consumer_secret=DS_CONFIG["ds_client_secret"],
            access_token_url=DS_CONFIG["authorization_server"] + "/oauth/token",
            authorize_url=DS_CONFIG["authorization_server"] + "/oauth/auth",
            request_token_params=request_token_params,
            base_url=None,
            request_token_url=None,
            access_token_method="POST"
        )

    @classmethod
    def _jwt_auth(cls, api):
        """JSON Web Token authorization"""
        api_client = ApiClient()
        api_client.set_base_path(DS_JWT["authorization_server"])

        use_scopes = []
        if api == "Rooms":
            use_scopes.extend(ROOMS_SCOPES)
        elif api == "Click":
            use_scopes.extend(CLICK_SCOPES)
        elif api == "Admin":
            use_scopes.extend(ADMIN_SCOPES)
        else:
            use_scopes.extend(SCOPES)
        # remove duplicate scopes
        use_scopes = list(set(use_scopes))

        use_scopes.append("impersonation")

        # Catch IO error
        try:
            private_key = get_private_key(DS_JWT["private_key_file"]).encode("ascii").decode("utf-8")
        except (OSError, IOError) as err:
            return render_template(
                "error.html",
                err=err
            )

        try:
            cls.ds_app = get_jwt_token(private_key, use_scopes, DS_JWT["authorization_server"], DS_JWT["ds_client_id"], DS_JWT["ds_impersonated_user_id"])
            return redirect(url_for("ds.ds_callback"))

        except ApiException as err:
            body = err.body.decode('utf8')

            # Grant explicit consent for the application
            if "consent_required" in body:
                consent_scopes = " ".join(use_scopes)
                redirect_uri = DS_CONFIG["app_url"] + url_for("ds.ds_callback")
                consent_url = f"{DS_CONFIG['authorization_server']}/oauth/auth?response_type=code&" \
                              f"scope={consent_scopes}&client_id={DS_JWT['ds_client_id']}&redirect_uri={redirect_uri}"
                return redirect(consent_url)
            else:
                process_error(err)

        return redirect(url_for("ds.ds_callback"))

    @classmethod
    def destroy(cls):
        cls.ds_app = None

    @classmethod
    def login(cls, auth_type, api):
        cls._init(auth_type, api)
        if auth_type == "code_grant":
            return cls.get(auth_type, api).authorize(callback=url_for("ds.ds_callback", _external=True))
        elif auth_type == "jwt":
            return cls._jwt_auth(api)

    @classmethod
    def get_token(cls, auth_type):
        resp = None
        if auth_type == "code_grant":
            resp = cls.get(auth_type).authorized_response()
        elif auth_type == "jwt":
            resp = cls.get(auth_type).to_dict()

        if resp is None or resp.get("access_token") is None:
            return "Access denied: reason=%s error=%s resp=%s" % (
                request.args["error"],
                request.args["error_description"],
                resp
            )

        return resp

    @classmethod
    def get_user(cls, access_token):
        """Make request to the API to get the user information"""
        # Determine user, account_id, base_url by calling OAuth::getUserInfo
        # See https://developers.docusign.com/esign-rest-api/guides/authentication/user-info-endpoints
        url = DS_CONFIG["authorization_server"] + "/oauth/userinfo"
        auth = {"Authorization": "Bearer " + access_token}
        response = requests.get(url, headers=auth).json()

        return response

    @classmethod
    def get(cls, auth_type, api=API_TYPE["ESIGNATURE"]):
        if not cls.ds_app:
            cls._init(auth_type, api)
        return cls.ds_app

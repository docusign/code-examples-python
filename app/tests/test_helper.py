import os
import base64
from enum import Enum
from docusign_esign import ApiClient
from docusign_esign.client.api_exception import ApiException
from .test_config import get_configuration

CONFIG = get_configuration()


class ApiType(Enum):
    ESIGN = "esignature"
    CLICK = "click"
    ROOMS = "rooms"
    MONITOR = "monitor"
    ADMIN = "admin"


class TestHelper:
    @staticmethod
    def authenticate(api_type=None):
        try:
            private_key_file = open(os.path.abspath(os.path.join(CONFIG["private_key_file"])), "r")
            private_key = private_key_file.read()

            api_client = ApiClient()
            api_client.host = CONFIG["base_path"]

            api_client = ApiClient()
            api_client.set_base_path(CONFIG["base_path"])
            api_client.set_oauth_host_name(CONFIG["oauth_base_path"])

            scopes = CONFIG["scopes"]

            if api_type is not None:
                if ApiType.ROOMS.value in api_type:
                    scopes.extend(CONFIG["rooms_scopes"])
                if ApiType.CLICK.value in api_type:
                    scopes.extend(CONFIG["click_scopes"])
                if ApiType.ADMIN.value in api_type:
                    scopes.extend(CONFIG["admin_scopes"])

                # remove duplicate scopes
                scopes = list(set(scopes))

            token_response = api_client.request_jwt_user_token(
                client_id=CONFIG["ds_client_id"],
                user_id=CONFIG["ds_impersonated_user_id"],
                oauth_host_name=CONFIG["oauth_base_path"],
                private_key_bytes=private_key,
                expires_in=CONFIG["expires_in"],
                scopes=scopes
            )

            access_token = token_response.access_token

            # Save API account ID
            user_info = api_client.get_user_info(access_token)
            accounts = user_info.get_accounts()
            api_account_id = accounts[0].account_id
            base_path = accounts[0].base_uri + "/restapi"

            return {"access_token": access_token, "account_id": api_account_id, "base_path": base_path}
        except ApiException as err:
            body = err.body.decode('utf8')

            if "consent_required" in body:
                url_scopes = "+".join(CONFIG["scopes"])
                url = f"https://{CONFIG['oauth_base_path']}/oauth/auth?response_type=code&" \
                      f"scope={url_scopes}&client_id={CONFIG['ds_client_id']}&redirect_uri={CONFIG['redirect_uri']}"

                consent_message = f"You should grant access by making the following call: {url}"
                print(consent_message)
                raise Exception(f"You should grant access by making the following call: {url}")

            raise err

    @staticmethod
    def read_as_base64(path):
        with open(path, "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        return base64_file_content

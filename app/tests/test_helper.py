import os
import base64
from docusign_esign import ApiClient
from docusign_esign.client.api_exception import ApiException

from ..ds_config import DS_CONFIG, DS_JWT

DATA = {
    "signer_client_id": '1000',
    "return_url": DS_CONFIG["app_url"] + "/ds-return",
    "ping_url": DS_CONFIG["app_url"] + "/",
    "private_key_filename": "../config/private.key",
    "base_path": 'https://demo.docusign.net/restapi',
    "oauth_base_path": 'account-d.docusign.com',
    "redirect_uri": 'https://www.docusign.com/api',
    "scopes": ["signature", "impersonation"],
    "expires_in": 3600,
    "test_pdf_file": './tests/docs/World_Wide_Corp_lorem.pdf',
    "test_docx_file": './tests/docs/World_Wide_Corp_Battle_Plan_Trafalgar.docx',
    "test_template_pdf_file": './tests/docs/World_Wide_Corp_fields.pdf',
    "test_template_docx_file": './tests/docs/World_Wide_Corp_salary.docx',
    "template_name": 'Example Signer and CC template',
    "cc_name": 'Test Name',
    "cc_email": 'test@mail.com',
    "item": 'Item',
    "quantity": '5'
}


class TestHelper:
    @staticmethod
    def authenticate():
        try:
            private_key_file = open(os.path.abspath(os.path.join("../", DS_JWT["private_key_file"])), "r")
            private_key = private_key_file.read()

            api_client = ApiClient()
            api_client.host = DATA["base_path"]

            api_client = ApiClient()
            api_client.set_base_path(DATA["base_path"])
            api_client.set_oauth_host_name(DATA["oauth_base_path"])
            token_response = api_client.request_jwt_user_token(
                client_id=DS_JWT["ds_client_id"],
                user_id=DS_JWT["ds_impersonated_user_id"],
                oauth_host_name=DATA["oauth_base_path"],
                private_key_bytes=private_key,
                expires_in=4000,
                scopes=DATA["scopes"]
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
                url_scopes = "+".join(DATA["scopes"])
                url = f"https://{DS_JWT['authorization_server']}/oauth/auth?response_type=code&" \
                      f"scope={url_scopes}&client_id={DS_JWT['ds_client_id']}&redirect_uri={DATA['redirect_uri']}"

                consent_message = f"You should grant access by making the following call: {url}"
                print(consent_message)
                raise Exception(f"You should grant access by making the following call: {url}")

    @staticmethod
    def read_as_base64(path):
        with open(path, "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        return base64_file_content


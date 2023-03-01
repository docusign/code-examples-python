import os
from dotenv import load_dotenv

load_dotenv()


def get_configuration():
    data = {
        "signer_client_id": '1000',
        "return_url": "http://localhost:5000/ds-return",
        "ping_url": "http://localhost:5000/",
        "private_key_filename": "./app/private.key",
        "base_path": 'https://demo.docusign.net/restapi',
        "oauth_base_path": 'account-d.docusign.com',
        "redirect_uri": 'https://www.docusign.com/api',
        "scopes": ["signature", "impersonation"],
        "expires_in": 3600,
        "test_pdf_file": './app/tests/docs/World_Wide_Corp_lorem.pdf',
        "test_docx_file": './app/tests/docs/World_Wide_Corp_Battle_Plan_Trafalgar.docx',
        "test_template_pdf_file": './app/tests/docs/World_Wide_Corp_fields.pdf',
        "test_template_docx_file": './app/tests/docs/World_Wide_Corp_salary.docx',
        "template_name": 'Example Signer and CC template',
        "cc_name": 'Test Name',
        "cc_email": 'test@mail.com',
        "item": 'Item',
        "quantity": '5'
    }

    if os.environ.get("CLIENT_ID") is not None:
        config = {
            "ds_client_id": os.environ.get("CLIENT_ID"),
            "ds_impersonated_user_id": os.environ.get("USER_ID"),
            "signer_email": os.environ.get("SIGNER_EMAIL"),
            "signer_name": os.environ.get("SIGNER_NAME"),
            "private_key_file": "./app/private.key"
        }
    else:
        from ..ds_config import DS_CONFIG, DS_JWT

        config = {
            "ds_client_id": DS_JWT["ds_client_id"],
            "ds_impersonated_user_id": DS_JWT["ds_impersonated_user_id"],
            "signer_email": DS_CONFIG["signer_email"],
            "signer_name": DS_CONFIG["signer_name"],
            "private_key_file": DS_JWT["private_key_file"]
        }

    return data | config

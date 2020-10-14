# ds_config.py
#
# DocuSign configuration settings

DS_CONFIG = {
    "ds_client_id": "{INTEGRATION_KEY_AUTH_CODE}",  # The app's DocuSign integration key
    "ds_client_secret": "{SECRET_KEY}",  # The app's DocuSign integration key's secret
    "signer_email": "{SIGNER_EMAIL}",
    "signer_name": "{SIGNER_NAME}",
    "app_url": "http://localhost:5000",  # The URL of the application. Eg http://localhost:5000
    # NOTE: You must add a Redirect URI of appUrl/ds/callback to your Integration Key.
    #       Example: http://localhost:5000/ds/callback
    "authorization_server": "https://account-d.docusign.com",
    "allow_silent_authentication": True,  # a user can be silently authenticated if they have an
    # active login session on another tab of the same browser
    "target_account_id": None,  # Set if you want a specific DocuSign AccountId,
    # If None, the user's default account will be used.
    "demo_doc_path": "demo_documents",
    "doc_salary_docx": "World_Wide_Corp_salary.docx",
    "doc_docx": "World_Wide_Corp_Battle_Plan_Trafalgar.docx",
    "doc_pdf": "World_Wide_Corp_lorem.pdf",
    # Payment gateway information is optional
    "gateway_account_id": "{DS_PAYMENT_GATEWAY_ID}",
    "gateway_name": "stripe",
    "gateway_display_name": "Stripe",
    "github_example_url": "https://github.com/docusign/code-examples-python/tree/master/app/",
    "documentation": "",  # Use an empty string to indicate no documentation path.
    "quickstart": "false"
}

DS_JWT = {
    "ds_client_id": "{INTEGRATION_KEY_JWT}",
    "ds_impersonated_user_id": "{IMPERSONATED_USER_ID}",  # The id of the user.
    "private_key_file": "./private.key", # Create a new file in your repo source folder named private.key then copy and paste your RSA private key there and save it.
    "authorization_server": "account-d.docusign.com"
}

EXAMPLES_API_TYPE = {
        "Rooms": True,
        "ESignature": False
}

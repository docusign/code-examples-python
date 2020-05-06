# ds_config.py
#
# DocuSign configuration settings

DS_CONFIG = {
    "ds_client_id": "{CLIENT_ID}",  # The app's DocuSign integration key
    "ds_client_secret": "{CLIENT_SECRET}",  # The app's DocuSign integration key's secret
    "signer_email": "{USER_EMAIL}",
    "signer_name": "{USER_FULLNAME}",
    "app_url": "{APP_URL}",  # The url of the application. Eg http://localhost:5000
    # NOTE: You must add a Redirect URI of appUrl/ds/callback to your Integration Key.
    #       Example: http:#localhost:5000/ds/callback
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
    "github_example_url": "https://github.com/docusign/eg-03-python-auth-code-grant/tree/master/app/",
    "documentation": ""  # Use an empty string to indicate no documentation path.
}

DS_JWT = {
    "ds_client_id": "{CLIENT_ID}",
    "ds_impersonated_user_id": "{IMPERSONATED_USER_ID}",  # the id of the user
    "private_key_file": "./private.key", # create a new file named private.key in the app directory
    "authorization_server": "account-d.docusign.com",
}

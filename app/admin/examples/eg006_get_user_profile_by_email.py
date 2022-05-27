from docusign_admin import ApiClient, UsersApi
from flask import session, request

from ...ds_config import DS_CONFIG
from app.admin.utils import get_organization_id

class Eg006GetUserProfileByEmailController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()
        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id, # Represents your {ORGANIZATION_ID},
            "email": request.form.get("email"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get user profile data
        """

        access_token = args["access_token"]
        org_id = args["organization_id"]
        email = args["email"]

        # Create an API client with headers
        # Step 2 start
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        # Step 2 end

        # Step 3 start
        users_api = UsersApi(api_client=api_client)

        results = users_api.get_user_ds_profiles_by_email(
            organization_id=org_id,
            email=email)
        # Step 3 end

        return results

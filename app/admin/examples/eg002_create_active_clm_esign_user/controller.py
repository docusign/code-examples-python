from docusign_orgadmin import ApiClient, ProductPermissionProfilesApi
from flask import session, json

from ....ds_config import DS_CONFIG

class Eg002Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get your monitor data via SDK
        """

        access_token = args["access_token"]
        account_id = args["account_id"]

        # Step 2 start
        # Create an API client with headers
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        # Step 2 end

        #Step 3 start
        product_permission_profiles_api = ProductPermissionProfilesApi(api_client=api_client)
        permission_profiles = product_permission_profiles_api.get_product_permission_profiles(organization_id=DS_CONFIG["organization_id"], account_id=session["ds_account_id"])
        print(permission_profiles)
        # Step 3 end

        # Step 4 start

        # Step 4 end

        # Step 5 start

        # Step 5 end

        return permission_profiles
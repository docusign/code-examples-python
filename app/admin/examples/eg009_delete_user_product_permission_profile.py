from docusign_admin import (
    ApiClient,
    ProductPermissionProfilesApi,
    UserProductProfileDeleteRequest)
from flask import session, request

from ...ds_config import DS_CONFIG
from app.admin.utils import get_organization_id

class Eg009DeleteUserProductPermissionProfileController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id,  # Represents your {ORGANIZATION_ID}
            "product_id": request.form.get("product_id"),
            "clm_email": session["clm_email"],
        }

    @staticmethod
    def get_permission_profiles_by_email():
        """Get permission profiles"""

        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {session['ds_access_token']}"
        )
        # Step 3 start
        product_permission_profiles_api = ProductPermissionProfilesApi(api_client=api_client)
        profiles = product_permission_profiles_api.get_user_product_permission_profiles_by_email(
            organization_id=get_organization_id(),
            account_id=session["ds_account_id"],
            email=session["clm_email"]
        )
        profiles_list = profiles.to_dict()["product_permission_profiles"]
        # Step 3 end
        return profiles_list

    @staticmethod
    def worker(self, args):
        """
        1. Create an API client with headers
        2. Get your monitor data via SDK
        """

        access_token = args["access_token"]
        account_id = args["account_id"]
        org_id = args["organization_id"]
        email = args["clm_email"]
        product_id = args["product_id"]

        # Create an API client with headers
        # Step 2 start        
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        # Step 2 end

        # Step 4 start
        user_product_profile_delete_request = UserProductProfileDeleteRequest(
            user_email=email,
            product_ids=[product_id]
        )
        # Step 4 end

        # Step 5 start
        product_permission_profiles_api = ProductPermissionProfilesApi(api_client=api_client)
        response = product_permission_profiles_api.remove_user_product_permission(
            organization_id=org_id,
            account_id=account_id,
            user_product_permission_profiles_request=user_product_profile_delete_request
        )
        # Step 5 end

        return response.to_dict()

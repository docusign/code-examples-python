from docusign_admin import (
    ApiClient,
    ProductPermissionProfilesApi,
    UserProductPermissionProfilesRequest,
    ProductPermissionProfileRequest)
from flask import session, request

from ...ds_config import DS_CONFIG
from app.admin.utils import get_organization_id

class Eg008UpdateUserProductPermissionProfileController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()

        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id,  # Represents your {ORGANIZATION_ID}
            "product_id": request.form.get("product"),
            "clm_email": session["clm_email"],
        }

    @staticmethod
    def get_permission_profiles():
        """Get permission profiles"""

        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {session['ds_access_token']}"
        )

        product_permission_profiles_api = ProductPermissionProfilesApi(api_client=api_client)
        profiles = product_permission_profiles_api.get_product_permission_profiles(
            organization_id=get_organization_id(),
            account_id=session["ds_account_id"]
        )
        profiles_list = profiles.to_dict()["product_permission_profiles"]
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
        clm_email = args["clm_email"]
        permission_profile_id = args["permission_profile_id"]
        product_id = args["product_id"]

        # Create an API client with headers
        #ds-snippet-start:Admin8Step2
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        #ds-snippet-end:Admin8Step2

        #ds-snippet-start:Admin8Step3
        product_permission_profile = ProductPermissionProfileRequest(
            permission_profile_id=permission_profile_id,
            product_id=product_id
        )
        user_product_permission_profile_request = UserProductPermissionProfilesRequest(
            email=clm_email,
            product_permission_profiles=[product_permission_profile]
        )
        #ds-snippet-end:Admin8Step3

        #ds-snippet-start:Admin8Step4
        product_permission_profiles_api = ProductPermissionProfilesApi(api_client=api_client)
        response = product_permission_profiles_api.add_user_product_permission_profiles_by_email(
            organization_id=org_id,
            account_id=account_id,
            user_product_permission_profiles_request=user_product_permission_profile_request
        )
        #ds-snippet-end:Admin8Step4

        return response.to_dict()

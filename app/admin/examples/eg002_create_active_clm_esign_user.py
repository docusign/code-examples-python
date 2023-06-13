from docusign_admin import ApiClient, ProductPermissionProfilesApi, DSGroupsApi, UsersApi, NewMultiProductUserAddRequest, ProductPermissionProfileRequest, DSGroupRequest
from flask import session, json, request

from ...ds_config import DS_CONFIG
from app.admin.utils import get_organization_id

class Eg002CreateActiveClmEsignUserController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()
        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id, # Represents your {ORGANIZATION_ID}
            "clm_permission_profile_name": request.form.get("clm_permission_profile"),
            "esign_permission_profile_name": request.form.get("esign_permission_profile"),
            "user_name": request.form.get("user_name"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "group_id": request.form.get("ds_group"),
        }

    @staticmethod
    def get_permission_profiles(args):
        """Get permission profiles"""

        access_token = args["access_token"]
        account_id = args["account_id"]
        org_id = args["organization_id"]

        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        #ds-snippet-start:Admin2Step3
        product_permission_profiles_api = ProductPermissionProfilesApi(api_client=api_client)
        profiles = product_permission_profiles_api.get_product_permission_profiles(organization_id=org_id, account_id=session["ds_account_id"])
        profiles_list = profiles.to_dict()["product_permission_profiles"]
        #ds-snippet-end:Admin2Step3
        return profiles_list

    @staticmethod
    def get_groups(args):
        """Get ds groups"""

        access_token = args["access_token"]
        account_id = args["account_id"]
        org_id = args["organization_id"]

        # Create an API client with headers
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )

        #ds-snippet-start:Admin2Step4
        ds_groups_api = DSGroupsApi(api_client)
        ds_groups = ds_groups_api.get_ds_groups(organization_id=org_id, account_id=session["ds_account_id"])
        #ds-snippet-end:Admin2Step4
        return ds_groups

    @staticmethod
    def worker(self, args):
        """
        1. Create an API client with headers
        2. Get your monitor data via SDK
        """

        access_token = args["access_token"]
        account_id = args["account_id"]
        org_id = args["organization_id"]
        clm_permission_profile_name = args["clm_permission_profile_name"]
        esign_permission_profile_name = args["esign_permission_profile_name"]

        # Create an API client with headers
        #ds-snippet-start:Admin2Step2      
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        #ds-snippet-end:Admin2Step2

        profiles_list = self.get_permission_profiles(args)

        for profile in profiles_list:
            if profile["product_name"] == "CLM":
                clm_product_id = profile["product_id"]
                for permission_profile in profile["permission_profiles"]:
                    if permission_profile["permission_profile_name"] == clm_permission_profile_name:
                        clm_permission_profile_id = permission_profile["permission_profile_id"]
            else:
                esign_product_id = profile["product_id"]
                for permission_profile in profile["permission_profiles"]:
                    if permission_profile["permission_profile_name"] == esign_permission_profile_name:
                        esign_permission_profile_id = permission_profile["permission_profile_id"]

        #ds-snippet-start:Admin2Step5
        clm_product_permission_profile = ProductPermissionProfileRequest(product_id=clm_product_id, permission_profile_id=clm_permission_profile_id)
        esign_product_permission_profile = ProductPermissionProfileRequest(product_id=esign_product_id, permission_profile_id=esign_permission_profile_id)
        ds_group_request = DSGroupRequest(ds_group_id=args["group_id"])
        new_user = NewMultiProductUserAddRequest(product_permission_profiles=[esign_product_permission_profile, clm_product_permission_profile], ds_groups=[ds_group_request], user_name=args["user_name"], first_name=args["first_name"], last_name=args["last_name"], email=args["email"], auto_activate_memberships=True)
        #ds-snippet-end:Admin2Step5

        #ds-snippet-start:Admin2Step6
        users_api = UsersApi(api_client)
        response = users_api.add_or_update_user(organization_id=org_id, account_id=session["ds_account_id"], request=new_user)
        #ds-snippet-end:Admin2Step6

        return response.to_dict()

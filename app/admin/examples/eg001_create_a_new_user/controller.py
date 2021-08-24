from docusign_admin import UsersApi, NewUserRequest, NewUserRequestAccountProperties, PermissionProfileRequest, GroupRequest
from docusign_esign import AccountsApi, ApiClient, GroupsApi
from flask import session

from app.admin.utils import create_admin_api_client
from app.consts import pattern
from app.ds_config import DS_CONFIG


class Eg001Controller:

    @staticmethod
    def get_args(request):
        """
        Get request and session arguments
        """

        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
            "user_name": request.form.get("user_name"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "user_email": request.form.get("user_email"),
            "permission_profile": request.form.get("profile_id"),
            "group": request.form.get("group_id")
        }

    @staticmethod
    def get_permission_profiles(args):
        """Get permission profiles"""

        access_token = args["access_token"]
        account_id = args["account_id"]

        api_client = ApiClient(host=session["ds_base_path"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        
        accounts_api = AccountsApi(api_client=api_client)
        profiles = accounts_api.list_permissions(account_id=account_id)
        profiles_list = profiles.to_dict()["permission_profiles"]

        return profiles_list

    @staticmethod
    def get_groups(args):
        """Get ds groups"""

        access_token = args["access_token"]
        account_id = args["account_id"]

        # Create an API client with headers
        api_client = ApiClient(host=session["ds_base_path"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )

        groups_api = GroupsApi(api_client)
        groups = groups_api.list_groups(account_id=account_id)
        groups_dict = groups.to_dict()
        groups_list = groups_dict["groups"]
        
        return groups_list

    @staticmethod
    def worker(self, args):
        """
        1. Create the API client object
        2. Create the user API request object
        3. Create a request body for the create_user method
        4. Creates a user using a method from the user API
        """

        # 1. Create the API client object 
        api_client = create_admin_api_client(
            access_token=session["ds_access_token"]
        )

        # 2. Create the user API request object
        user_api = UsersApi(api_client=api_client)

        # Get group information
        groups = self.get_groups(args)
        for group in groups:
            if group["group_id"] == args["group"]:
                group_name = group["group_name"]
                group_type = group["group_type"]

        # Get permission profile information
        permission_profiles = self.get_permission_profiles(args)
        for profile in permission_profiles:
            if profile["permission_profile_id"] == args["permission_profile"]:
                profile_name = profile["permission_profile_name"]

        # 3. Create a request body for the create_user method 

        request_body = {
            "user_name": args["user_name"],
            "first_name": args['first_name'],
            "last_name": args['last_name'],
            "email": args['user_email'],
            "auto_activate_memberships": True,
            "accounts": [
                {
                    "id": session["ds_account_id"],
                    "permission_profile": {
                        "id": args['permission_profile'],
                    },
                    "groups": [
                        {
                            "id": args["group"],
                        }
                    ]
                }
            ]
        }

        # 4. Creates a user using a method from the user API
        response = user_api.create_user(
            DS_CONFIG["organization_id"],
            request_body
        )
        return response

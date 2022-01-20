from docusign_esign import AccountsApi, Group, GroupInformation, GroupsApi
from docusign_esign.client.api_exception import ApiException
from flask import session, request
from ...docusign import create_api_client
from ...error_handlers import process_error

class Eg025PermissionsSetUserGroupController:
    @staticmethod
    def get_args():
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "permission_profile_id": request.form.get("permission_profile"),
            "group_id": request.form.get("group")
        }

    @staticmethod
    def worker(args):
        """
        Step 1: Create an API client
        Step 2: Create a group object
        Step 3: Create a group information object
        Step 4: Update the group
        """

        # Step 2. Construct your API headers
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        group_api = GroupsApi(api_client)

        # Step 3. Construct your request body
        group = Group(group_id=args["group_id"], permission_profile_id=args["permission_profile_id"])
        group_information = GroupInformation(groups=[group])

        # Step 4. Call the eSignature REST API
        response = group_api.update_groups(account_id=args["account_id"], group_information=group_information)

        return response

    @staticmethod
    def get_data(args):
        """Retrieve groups and permission profiles"""
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        try:
            account_api = AccountsApi(api_client)
            group_api = GroupsApi(api_client)
            permission_profiles = account_api.list_permissions(account_id=args["account_id"]).permission_profiles
            groups = group_api.list_groups(account_id=args["account_id"]).groups

            return permission_profiles, groups

        except ApiException as err:
            return process_error(err)
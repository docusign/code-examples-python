from datetime import datetime as dt, timezone
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

        # Construct your API headers
        #ds-snippet-start:eSign25Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        group_api = GroupsApi(api_client)
        #ds-snippet-end:eSign25Step2

        # Construct your request body
        #ds-snippet-start:eSign25Step3
        group = Group(group_id=args["group_id"], permission_profile_id=args["permission_profile_id"])
        group_information = GroupInformation(groups=[group])
        #ds-snippet-end:eSign25Step3

        # Call the eSignature REST API
        #ds-snippet-start:eSign25Step4
        (response, status, headers) = group_api.update_groups_with_http_info(account_id=args["account_id"], group_information=group_information)

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:eSign25Step4

        return response

    @staticmethod
    def get_data(args):
        """Retrieve groups and permission profiles"""
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        try:
            account_api = AccountsApi(api_client)
            group_api = GroupsApi(api_client)
            (permission_profiles, status, headers) = account_api.list_permissions_with_http_info(account_id=args["account_id"]).permission_profiles

            remaining = headers.get("X-RateLimit-Remaining")
            reset = headers.get("X-RateLimit-Reset")

            if remaining is not None and reset is not None:
                reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
                print(f"API calls remaining: {remaining}")
                print(f"Next Reset: {reset_date}")
            
            (groups, status, headers) = group_api.list_groups_with_http_info(account_id=args["account_id"]).groups

            remaining = headers.get("X-RateLimit-Remaining")
            reset = headers.get("X-RateLimit-Reset")

            if remaining is not None and reset is not None:
                reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
                print(f"API calls remaining: {remaining}")
                print(f"Next Reset: {reset_date}")

            return permission_profiles, groups

        except ApiException as err:
            return process_error(err)
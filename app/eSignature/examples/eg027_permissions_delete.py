from docusign_esign import AccountsApi
from docusign_esign.client.api_exception import ApiException
from flask import session, request
from ...docusign import create_api_client
from ...error_handlers import process_error

class Eg027PermissionsDeleteController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "permission_profile_id": request.form.get("permission_profile"),
        }

    @staticmethod
    def worker(args):
        """
        Step 1: Create an API client
        Step 2: Delete the permission profile using SDK
        """
        
        # Step 2. Construct your API headers
        #ds-snippet-start:eSign27Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        account_api = AccountsApi(api_client)
        #ds-snippet-end:eSign27Step2
        
        # Step 3. Call the eSignature REST API
        account_api.delete_permission_profile(
            account_id=args["account_id"],
            permission_profile_id=args["permission_profile_id"])

    @staticmethod
    def get_permissions_profiles(args):
        """Retrieve all permissions profiles"""
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        try:
            account_api = AccountsApi(api_client)
            response = account_api.list_permissions(account_id=args["account_id"])

            return response.permission_profiles

        except ApiException as err:
            return process_error(err)

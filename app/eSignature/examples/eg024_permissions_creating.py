from docusign_esign import AccountsApi, PermissionProfile
from flask import session, request

from ...consts import settings
from ...docusign import create_api_client


class Eg024PermissionsCreatingController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        args = {
            "account_id": session["ds_account_id"],  # represent your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # represent your {ACCESS_TOKEN}
            "permission_profile_name": request.form.get("permission_profile_name"),
            "settings": settings
        }
        return args

    @staticmethod
    def worker(args):
        """
        1. Create an api client
        2. Create a permission profile object
        3. Create the permission profile using the SDK
        """

        # Step 2. Construct your API request headers
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        # Step 3. Construct your request body
        permission_profile = PermissionProfile(
            permission_profile_name=args["permission_profile_name"],
            settings=args["settings"]
        )

        # Step 4. Call the eSignature REST API
        account_api = AccountsApi(api_client)
        response = account_api.create_permission_profile(
            account_id=args["account_id"],
            permission_profile=permission_profile
        )

        return response

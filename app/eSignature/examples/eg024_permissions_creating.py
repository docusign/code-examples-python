from datetime import datetime as dt, timezone
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

        # Construct your API request headers
        #ds-snippet-start:eSign24Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign24Step2

        # Construct your request body
        #ds-snippet-start:eSign24Step3
        permission_profile = PermissionProfile(
            permission_profile_name=args["permission_profile_name"],
            settings=args["settings"]
        )
        #ds-snippet-end:eSign24Step3

        # Call the eSignature REST API
        #ds-snippet-start:eSign24Step4
        account_api = AccountsApi(api_client)
        (response, status, headers) = account_api.create_permission_profile_with_http_info(
            account_id=args["account_id"],
            permission_profile=permission_profile
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:eSign24Step4

        return response

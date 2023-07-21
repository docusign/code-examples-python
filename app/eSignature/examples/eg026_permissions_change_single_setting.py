from docusign_esign import AccountsApi, PermissionProfile
from docusign_esign.client.api_exception import ApiException
from flask import request, session
from ...consts import settings
from ...docusign import create_api_client
from ...error_handlers import process_error

class Eg026PermissionsChangeSingleSettingController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        permission_profile_id = request.form.get("permission_profile")
        args = {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "permission_profile_id": permission_profile_id,
            "settings": settings
        }
        return args

    @staticmethod
    def worker(args):
        """
        1. Create an API client
        2. Create a permission profile object
        3. Get existing profile settings
        4. Change the permission profile setting using the SDK
        """

        # Step 2. Construct your API headers
        #ds-snippet-start:eSign26Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign26Step2

        # Step 3. Construct your request body
        #ds-snippet-start:eSign26Step3
        permission_profile = PermissionProfile(
            settings=args["settings"]
        )
        account_api = AccountsApi(api_client)
        previous_settings = account_api.get_permission_profile(
            account_id=args["account_id"],
            permission_profile_id=args["permission_profile_id"]
        ).settings.to_dict()
        #ds-snippet-end:eSign26Step3
        # Step 4. Call the eSignature REST API
        #ds-snippet-start:eSign26Step4
        response = account_api.update_permission_profile(
            account_id=args["account_id"],
            permission_profile_id=args["permission_profile_id"],
            permission_profile=permission_profile
        )
        new_settings = response.settings.to_dict()
        #ds-snippet-end:eSign26Step4
        changed_settings = {}

        # Save only changed settings
        for k, v in new_settings.items():
            if v != previous_settings[k]:
                key = " ".join(k.split("_"))
                changed_settings[key] = v

        return response, changed_settings

    @staticmethod
    def get_permissions_profiles(args):
        """Retrieve all permissions profiles"""
        api_client = create_api_client(
            base_path=args["base_path"],
            access_token=args["access_token"]
        )

        try:
            account_api = AccountsApi(api_client)
            response = account_api.list_permissions(account_id=args["account_id"])

            return response.permission_profiles

        except ApiException as err:
            return process_error(err)
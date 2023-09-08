from docusign_admin import ApiClient, ProvisionAssetGroupApi, AssetGroupAccountClone, \
    AssetGroupAccountCloneSourceAccount, AssetGroupAccountCloneTargetAccount, \
    AssetGroupAccountCloneTargetAccountAdmin
from flask import session, request

from ..utils import get_organization_id
from ...ds_config import DS_CONFIG


class Eg012CloneAccountController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()

        return {
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id,
            "source_account_id": request.form.get("source_account_id"),
            "target_account_name": request.form.get("target_account_name"),
            "target_account_user_name": request.form.get("target_account_user_name"),
            "target_account_first_name": request.form.get("target_account_first_name"),
            "target_account_last_name": request.form.get("target_account_last_name"),
            "target_account_email": request.form.get("target_account_email"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get the list of eligible accounts
        3. Construct the request body
        4. Clone the account
        """

        access_token = args["access_token"]

        # Create an API client with headers
        #ds-snippet-start:Admin12Step2
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        #ds-snippet-end:Admin12Step2

        #ds-snippet-start:Admin12Step4
        account_data = AssetGroupAccountClone(
            source_account=AssetGroupAccountCloneSourceAccount(
                id=args["source_account_id"]
            ),
            target_account=AssetGroupAccountCloneTargetAccount(
                name=args["target_account_name"],
                admin=AssetGroupAccountCloneTargetAccountAdmin(
                    first_name=args["target_account_first_name"],
                    last_name=args["target_account_last_name"],
                    email=args["target_account_email"]
                ),
                country_code="US"
            )
        )
        #ds-snippet-end:Admin12Step4

        #ds-snippet-start:Admin12Step5
        asset_group_api = ProvisionAssetGroupApi(api_client=api_client)
        results = asset_group_api.clone_asset_group_account(args["organization_id"], account_data)
        #ds-snippet-end:Admin12Step5

        return results

    @staticmethod
    def get_accounts(args):
        access_token = args["access_token"]
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )

        #ds-snippet-start:Admin12Step3
        asset_group_api = ProvisionAssetGroupApi(api_client=api_client)
        accounts = asset_group_api.get_asset_group_accounts(args["organization_id"], compliant=True)
        #ds-snippet-end:Admin12Step3

        return accounts

from docusign_admin import ApiClient, ProvisionAssetGroupApi, SubAccountCreateRequest, \
    SubAccountCreateRequestSubAccountCreationSubscription, \
    SubAccountCreateRequestSubAccountCreationTargetAccountDetails, \
    SubAccountCreateRequestSubAccountCreationTargetAccountAdmin
from flask import session, request

from ..utils import get_organization_id
from ...ds_config import DS_CONFIG


class Eg013CreateAccountController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()

        return {
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id,
            "base_path": DS_CONFIG["admin_api_client_host"],
            "email": request.form.get("email"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "subscription_id": session.get("subscription_id"),
            "plan_id": session.get("plan_id"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get the list of eligible accounts
        3. Construct the request body
        4. Create the account
        """

        access_token = args["access_token"]

        # Create an API client with headers
        #ds-snippet-start:Admin13Step2
        api_client = ApiClient(host=args["base_path"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        #ds-snippet-end:Admin13Step2

        #ds-snippet-start:Admin13Step4
        account_data = SubAccountCreateRequest(
            subscription_details=SubAccountCreateRequestSubAccountCreationSubscription(
                id=args["subscription_id"],
                plan_id=args["plan_id"],
                modules=[]
            ),
            target_account=SubAccountCreateRequestSubAccountCreationTargetAccountDetails(
                name="CreatedThroughAPI",
                country_code="US",
                admin=SubAccountCreateRequestSubAccountCreationTargetAccountAdmin(
                    email=args["email"],
                    first_name=args["first_name"],
                    last_name=args["last_name"],
                    locale="en"
                )
            )
        )
        #ds-snippet-end:Admin13Step4

        #ds-snippet-start:Admin13Step5
        asset_group_api = ProvisionAssetGroupApi(api_client=api_client)
        results = asset_group_api.create_asset_group_account(args["organization_id"], account_data)
        #ds-snippet-end:Admin13Step5

        return results

    @staticmethod
    def get_organization_plan_items(args):
        access_token = args["access_token"]
        api_client = ApiClient(host=args["base_path"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )

        #ds-snippet-start:Admin13Step3
        asset_group_api = ProvisionAssetGroupApi(api_client=api_client)
        plan_items = asset_group_api.get_organization_plan_items(args["organization_id"])
        #ds-snippet-end:Admin13Step3

        return plan_items

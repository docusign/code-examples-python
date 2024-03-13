from docusign_admin import ApiClient, AccountsApi, IndividualMembershipDataRedactionRequest
from flask import session, request

from ...ds_config import DS_CONFIG


class Eg011DeleteUserDataFromAccountController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "user_id": request.form.get("user_id"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Delete user data
        """

        access_token = args["access_token"]
        account_id = args["account_id"]
        user_id = args["user_id"]

        # Create an API client with headers
        #ds-snippet-start:Admin11Step2
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        #ds-snippet-end:Admin11Step2

        #ds-snippet-start:Admin11Step3
        accounts_api = AccountsApi(api_client=api_client)
        membership_redaction_request = IndividualMembershipDataRedactionRequest(user_id=user_id)
        #ds-snippet-end:Admin11Step3

        #ds-snippet-start:Admin11Step4
        results = accounts_api.redact_individual_membership_data(account_id, membership_redaction_request)
        #ds-snippet-end:Admin11Step4

        return results

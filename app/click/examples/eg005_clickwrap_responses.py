from docusign_click import AccountsApi
from flask import request, session

from ..utils import create_click_api_client


class Eg005ClickwrapResponsesController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
            "clickwrap_id": request.form.get("clickwrap_id"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get clickwrap responses using SDK
        """
        # Step 1. Create an API client with headers
        #ds-snippet-start:Click5Step2
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )
        #ds-snippet-end:Click5Step2

        # Step 2. Get clickwrap responses using SDK
        #ds-snippet-start:Click5Step3
        accounts_api = AccountsApi(api_client)
        response = accounts_api.get_clickwrap_agreements(
            account_id=args["account_id"],
            clickwrap_id=args["clickwrap_id"],
            status="agreed"
        )
        #ds-snippet-end:Click5Step3

        return response

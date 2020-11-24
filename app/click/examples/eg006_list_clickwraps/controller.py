from docusign_click import AccountsApi, ClickwrapRequest
from flask import session

from ...utils import create_click_api_client


class Eg006Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get a list of all clickwraps
        """
        # Step 1. Create an API client with headers
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )

        # Step 2. Get a list of all clickwraps
        accounts_api = AccountsApi(api_client)
        response = accounts_api.get_clickwraps(
            account_id=args["account_id"]
        )

        return response

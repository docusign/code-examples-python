from docusign_click import AccountsApi, ClickwrapRequest
from flask import session

from ..utils import create_click_api_client


class Eg004ListClickwrapsController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
        }

    @staticmethod
    def worker(args):
        """
        Create an API client with headers
        Get a list of all elastic templates
        """
        # Create an API client with headers
        #ds-snippet-start:Click4Step2
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )
        #ds-snippet-end

        # Get a list of all elastic templates
        #ds-snippet-start:Click4Step3
        accounts_api = AccountsApi(api_client)
        response = accounts_api.get_clickwraps(
            account_id=args["account_id"]
        )
        #ds-snippet-end

        return response

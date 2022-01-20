from docusign_click import AccountsApi, ClickwrapRequest
from flask import session

from ..utils import create_click_api_client


class Eg002ActivateClickwrapController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
            "clickwrap_id": session.get("clickwrap_id"),
            "clickwrap_name": session.get("clickwrap_name"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create a clickwrap request model
        3. Update a clickwrap using SDK
        """
        # Step 1. Create an API client with headers
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )

        # Step 2. Create a clickwrap request model
        clickwrap_request = ClickwrapRequest(status="active")

        # Step 3. Update a clickwrap using SDK
        accounts_api = AccountsApi(api_client)
        response = accounts_api.update_clickwrap_version(
            account_id=args["account_id"],
            clickwrap_id=args["clickwrap_id"],
            clickwrap_request=clickwrap_request,
            version_id="1"
        )

        return response

from docusign_click import AccountsApi, ClickwrapRequest
from flask import session, request
import ast

from ..utils import create_click_api_client


class Eg002ActivateClickwrapController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
            "clickwrap": request.form.get("clickwrap"),
            "statuses": ["inactive", "draft"]
        }
        
    @staticmethod
    def get_inactive_clickwraps(args):
        """
        1. Create an API client with hheaders
        2. Get a list of inactive clickwraps
        """
        # Step 1. Create an API client with headers
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )
        
        # Step 2. Get a list of inactive clickwraps
        accounts_api = AccountsApi(api_client)
        clickwraps = []

        for status in args["statuses"]:
            response = accounts_api.get_clickwraps(
                account_id=args["account_id"],
                status=status
            )
            clickwraps += response.clickwraps

        return {"clickwraps": clickwraps}

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create a clickwrap request model
        3. Update a clickwrap using SDK
        """
        # Step 1. Create an API client with headers
        #ds-snippet-start:Click2Step2
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )
        #ds-snippet-end:Click2Step2

        # Step 2. Create a clickwrap request model
        #ds-snippet-start:Click2Step3
        clickwrap_request = ClickwrapRequest(status="active")
        #ds-snippet-end:Click2Step3

        # Step 3. Update a clickwrap using SDK
        #ds-snippet-start:Click2Step4
        accounts_api = AccountsApi(api_client)
        #ds-snippet-end:Click2Step4
        clickwrap = ast.literal_eval(args["clickwrap"])
        print(type(clickwrap))
        #ds-snippet-start:Click2Step4
        response = accounts_api.update_clickwrap_version(
            account_id=args["account_id"],
            clickwrap_id=clickwrap["clickwrap_id"],
            version_id=clickwrap["version_number"],
            clickwrap_request=clickwrap_request,
        )
        #ds-snippet-end:Click2Step4

        return response

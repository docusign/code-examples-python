from docusign_click import AccountsApi, UserAgreementRequest
from flask import session, request
import ast

from ..utils import create_click_api_client


class Eg006EmbedClickwrapController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
            "clickwrap": request.form.get("clickwrap"),
            "fullName": request.form.get("fullName"),
            "email": request.form.get("email"),
            "company": request.form.get("company"),
            "title": request.form.get("title"),
            "date": request.form.get("date"),            
        }     

    @staticmethod
    def get_active_clickwraps(args):
        """
        1. Create an API client with hheaders
        2. Get a list of active clickwraps
        """
        # Step 1. Create an API client with headers
        #ds-snippet-start:Click6Step2
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )
        #ds-snippet-end:Click6Step2
        
        # Step 2. Get a list of active clickwraps
        accounts_api = AccountsApi(api_client)
        response = accounts_api.get_clickwraps(
            account_id=args["account_id"],
            status="active"
        )
        
        return response

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create a clickwrap request model
        3. Update a clickwrap using SDK
        """
        # Create an API client with headers
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )
        
        # Create a user agreement request model
        #ds-snippet-start:Click6Step3
        user_agreement_request = UserAgreementRequest(
            client_user_id=args["email"],
            document_data={
                "fullName": args["fullName"],
                "email": args["email"],
                "company": args["company"],
                "title": args["title"],
                "date": args["date"]
            },
        )
        #ds-snippet-end:Click6Step3

        # Retrieve Agreement URL using SDK
        #ds-snippet-start:Click6Step4
        accounts_api = AccountsApi(api_client)
        clickwrap = ast.literal_eval(args["clickwrap"])
        print(type(clickwrap))
        response = accounts_api.create_has_agreed(
            account_id=args["account_id"],
            clickwrap_id=clickwrap["clickwrap_id"],
            user_agreement_request=user_agreement_request,
        )
        #ds-snippet-end:Click6Step4

        return response

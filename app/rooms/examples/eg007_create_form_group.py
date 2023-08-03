from docusign_rooms import FormGroupForCreate, FormGroupsApi
from flask import session, request

from app.rooms import create_rooms_api_client

class Eg007CreateFormGroupController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],     # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "form_group_name": request.form.get("form_group_name"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create FormGroupForCreate object
        3. POST the form using SDK
        """
        # Create an API with headers
        #ds-snippet-start:Rooms7Step2
        api_client = create_rooms_api_client(access_token=args["access_token"])
        #ds-snippet-end:Rooms7Step2
        # Create FormGroupForCreate object
        #ds-snippet-start:Rooms7Step3
        form = FormGroupForCreate(name=args["form_group_name"])
        #ds-snippet-end:Rooms7Step3
        # Post the form object using SDK
        #ds-snippet-start:Rooms7Step4
        form_groups_api = FormGroupsApi(api_client)
        response = form_groups_api.create_form_group(
            body=form, account_id=args["account_id"]
        )
        #ds-snippet-end:Rooms7Step4

        return response
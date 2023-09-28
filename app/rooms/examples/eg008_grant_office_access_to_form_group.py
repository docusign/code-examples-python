from docusign_rooms import (
    FormGroupsApi,
    FormGroupSummaryList,
    OfficesApi,
    OfficeSummaryList,
)
from flask import session, request

from app.rooms import create_rooms_api_client


class Eg008GrantOfficeAccessToFormGroupController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "form_group_id": request.form.get("form_group_id"),
            "office_id": request.form.get("office_id")
        }

    @staticmethod
    def get_form_groups(args):
        """
        1. Create an API Client with headers
        2. GET Form Groups via FormGroupsAPI
        """

        api_client = create_rooms_api_client(access_token=args["access_token"])

        # GET Form Groups via FormGroupsAPI
        #ds-snippet-start:Rooms8Step4
        form_groups_api = FormGroupsApi(api_client)
        response = form_groups_api.get_form_groups(account_id=args["account_id"])  # type: FormGroupSummaryList

        return response.form_groups
        #ds-snippet-end:Rooms8Step4        

    @staticmethod
    def get_offices(args):
        """
        1. Create an API Client with headers
        2. Get Offices via OfficesAPI
        """

        # Create an API with headers with headers
        #ds-snippet-start:Rooms8Step2
        api_client = create_rooms_api_client(args["access_token"])
        #ds-snippet-end:Rooms8Step2

        # GET offices via OfficesAPI
        #ds-snippet-start:Rooms8Step3
        offices_api = OfficesApi(api_client=api_client)
        response = offices_api.get_offices(account_id=args["account_id"])  # type: OfficeSummaryList

        return response.office_summaries
        #ds-snippet-end:Rooms8Step3

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Grant office access to a form group via FormGroups API
        """
        # Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Grant office access to a form group via FormGroups API
        #ds-snippet-start:Rooms8Step5
        form_groups_api = FormGroupsApi(api_client)

        form_groups_api.grant_office_access_to_form_group(
            form_group_id=args["form_group_id"], office_id=args["office_id"],
            account_id=args["account_id"]
        )
        #ds-snippet-end:Rooms8Step5

from datetime import datetime as dt, timezone
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
        (response, status, headers) = form_groups_api.get_form_groups_with_http_info(account_id=args["account_id"])  # type: FormGroupSummaryList

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

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
        (response, status, headers) = offices_api.get_offices_with_http_info(account_id=args["account_id"])  # type: OfficeSummaryList

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

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

        (response, status, headers) = form_groups_api.grant_office_access_to_form_group_with_http_info(
            form_group_id=args["form_group_id"], office_id=args["office_id"],
            account_id=args["account_id"]
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms8Step5

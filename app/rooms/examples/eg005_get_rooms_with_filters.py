from docusign_rooms import RoomsApi
from datetime import datetime as dt, timezone
from flask import session, request

from ..utils import create_rooms_api_client


class Eg005GetRoomsWithFiltersController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date")
        }

    @staticmethod
    def get_rooms(args):
        """
        1. Create an API client with headers
        2. Get rooms with filter
        """
        # Step 1. Create an API client with headers
        #ds-snippet-start:Rooms5Step2
        api_client = create_rooms_api_client(access_token=args["access_token"])
        #ds-snippet-end:Rooms5Step2

        # Step 2. Get room templates
        #ds-snippet-start:Rooms5Step4
        rooms_api = RoomsApi(api_client)
        (rooms, status, headers) = rooms_api.get_rooms_with_http_info(account_id=args["account_id"])

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        #ds-snippet-end:Rooms5Step4
        return rooms.rooms

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get room field data using SDK
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get room field data using SDK
        rooms_api = RoomsApi(api_client)
        (response, status, headers) = rooms_api.get_rooms_with_http_info(
            account_id=args["account_id"],
            #ds-snippet-start:Rooms5Step3
            field_data_changed_start_date=dt.strptime(args['start_date'], "%Y-%m-%d"),
            field_data_changed_end_date=dt.strptime(args['end_date'], "%Y-%m-%d"),
            #ds-snippet-end:Rooms5Step3
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        return response

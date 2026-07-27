from datetime import datetime as dt, timezone
from docusign_rooms import RoomsApi
from flask import session, request

from ..utils import create_rooms_api_client


class Eg003ExportDataFromRoomController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "room_id": request.form.get("room_id"),
        }

    @staticmethod
    def get_rooms(args):
        """
        1. Create an API client with headers
        2. Get rooms
        """
        # Step 1. Create an API client with headers
        #ds-snippet-start:Rooms3Step2
        api_client = create_rooms_api_client(access_token=args["access_token"])
        #ds-snippet-end:Rooms3Step2

        # Step 2. Get room templates
        rooms_api = RoomsApi(api_client)
        (rooms, status, headers) = rooms_api.get_rooms_with_http_info(account_id=args["account_id"])

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

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
        #ds-snippet-start:Rooms3Step3
        rooms_api = RoomsApi(api_client)
        (response, status, headers) = rooms_api.get_room_field_data_with_http_info(
            room_id=args['room_id'],
            account_id=args["account_id"]
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms3Step3

        return response

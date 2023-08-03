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
        rooms = rooms_api.get_rooms(account_id=args["account_id"])
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
        response = rooms_api.get_room_field_data(
            room_id=args['room_id'],
            account_id=args["account_id"]
        )
        #ds-snippet-end:Rooms3Step3
        return response

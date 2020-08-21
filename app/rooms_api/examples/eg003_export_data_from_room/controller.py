from docusign_rooms import ApiClient, RoomsApi
from flask import session, request


class Eg003Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
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
        api_client = ApiClient(host="https://demo.rooms.docusign.com/restapi")
        api_client.set_default_header(header_name="Authorization",
                                      header_value=f"Bearer {args['access_token']}")

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
        api_client = ApiClient(host="https://demo.rooms.docusign.com/restapi")
        api_client.set_default_header(header_name="Authorization",
                                      header_value=f"Bearer {args['access_token']}")

        # Step 2. Get room field data using SDK
        rooms_api = RoomsApi(api_client)
        response = rooms_api.get_room_field_data(
            room_id=args['room_id'],
            account_id=args["account_id"]
        )
        return response

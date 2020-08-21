from datetime import datetime
from docusign_rooms import ApiClient, RoomsApi
from flask import session, request


class Eg005Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
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
        response = rooms_api.get_rooms(
            account_id=args["account_id"],
            field_data_changed_start_date=datetime.strptime(args['start_date'], "%Y-%m-%d"),
            field_data_changed_end_date=datetime.strptime(args['end_date'], "%Y-%m-%d"),
        )
        return response

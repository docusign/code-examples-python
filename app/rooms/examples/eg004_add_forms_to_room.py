from docusign_rooms import FormForAdd, FormLibrariesApi, RoomsApi
from flask import session, request

from ..utils import create_rooms_api_client


class Eg004AddFormsToRoomController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "room_id": request.form.get("room_id"),
            "form_id": request.form.get("form_id"),
        }

    @staticmethod
    def get_rooms(args):
        """
        1. Create an API client with headers
        2. Get rooms
        """
        # Step 1. Create an API client with headers
        #ds-snippet-start:Rooms4Step2
        api_client = create_rooms_api_client(access_token=args["access_token"])
        #ds-snippet-end:Rooms4Step2

        # Step 2. Get rooms
        rooms_api = RoomsApi(api_client)
        rooms = rooms_api.get_rooms(account_id=args["account_id"])
        return rooms.rooms

    @staticmethod
    def get_forms(args):
        """
        1. Create an API client with headers
        2. Get first form library id
        3. Get forms
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get first form library id
        #ds-snippet-start:Rooms4Step3
        form_libraries_api = FormLibrariesApi(api_client)
        form_libraries = form_libraries_api.get_form_libraries(account_id=args["account_id"])
        first_form_library_id = form_libraries.forms_library_summaries[0].forms_library_id
        #ds-snippet-end:Rooms4Step3

        # Step 3. Get forms
        #ds-snippet-start:Rooms4Step2
        form_library_forms = form_libraries_api.get_form_library_forms(
            form_library_id=first_form_library_id,
            account_id=args["account_id"]
        )
        #ds-snippet-end:Rooms4Step3
        return form_library_forms.forms

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Add the form to the room
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Add the form to the room
        #ds-snippet-start:Rooms4Step4
        rooms_api = RoomsApi(api_client)
        response = rooms_api.add_form_to_room(
            room_id=args['room_id'],
            body=FormForAdd(form_id=args['form_id']),
            account_id=args["account_id"]
        )
        #ds-snippet-end:Rooms4Step4
        return response
from datetime import datetime as dt, timezone
from docusign_rooms import (
    ExternalFormFillSessionsApi,
    ExternalFormFillSessionForCreate,
    FormLibrariesApi,
    RoomsApi
)
from flask import session, request

from ..utils import create_rooms_api_client


class Eg006CreateExternalFormFillSessionController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "room_id": request.form.get("room_id"),
            "form_id": request.form.get("form_id"),
            "x_frame_allowed_url": "http://localhost:3000"
        }

    @staticmethod
    def get_rooms(args):
        """
        1. Create an API client with headers
        2. Get rooms
        """
        # Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Get rooms
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
    def get_room(args):
        """
        1. Create an API client with headers
        2. Get room by id
        """
        # Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Get room by id
        rooms_api = RoomsApi(api_client)
        (room, status, headers) = rooms_api.get_room_with_http_info(
            room_id=args["room_id"],
            account_id=args["account_id"]
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        return room

    @staticmethod
    def get_forms(args):
        """
        1. Create an API client with headers
        2. Get room documents
        2. Get room forms
        """
        # Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Get room documents
        rooms_api = RoomsApi(api_client)
        (room_documents, status, headers) = rooms_api.get_documents_with_http_info(
            room_id=args["room_id"],
            account_id=args["account_id"]
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        # Get room forms
        room_forms = [
            form for form in room_documents.documents
            if form.docu_sign_form_id
        ]
        return room_forms

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create an external form fill session
        """
        # Create an API client with headers
        #ds-snippet-start:Rooms6Step2
        api_client = create_rooms_api_client(access_token=args["access_token"])
        #ds-snippet-end:Rooms6Step2
        
        #ds-snippet-start:Rooms6Step3
        request_body = ExternalFormFillSessionForCreate(
            room_id=args['room_id'],
            form_id=args['form_id'],
            x_frame_allowed_url=args['x_frame_allowed_url']
        )
        #ds-snippet-end:Rooms6Step3

        # Create an external form fill session
        #ds-snippet-start:Rooms6Step4
        form_fill_session_api = ExternalFormFillSessionsApi(api_client)
        (results, status, headers) = form_fill_session_api.create_external_form_fill_session_with_http_info(
            body=request_body,
            account_id=args["account_id"]
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms6Step4

        return results

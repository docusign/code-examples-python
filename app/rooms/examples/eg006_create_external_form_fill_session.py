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
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get rooms
        rooms_api = RoomsApi(api_client)
        rooms = rooms_api.get_rooms(account_id=args["account_id"])
        return rooms.rooms

    @staticmethod
    def get_room(args):
        """
        1. Create an API client with headers
        2. Get room by id
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get room by id
        rooms_api = RoomsApi(api_client)
        room = rooms_api.get_room(
            room_id=args["room_id"],
            account_id=args["account_id"]
        )
        return room

    @staticmethod
    def get_forms(args):
        """
        1. Create an API client with headers
        2. Get room documents
        2. Get room forms
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get room documents
        rooms_api = RoomsApi(api_client)
        room_documents = rooms_api.get_documents(
            room_id=args["room_id"],
            account_id=args["account_id"]
        )

        # Step 2. Get room forms
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
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])
        
        request_body = ExternalFormFillSessionForCreate(
            room_id=args['room_id'],
            form_id=args['form_id'],
            x_frame_allowed_url=args['x_frame_allowed_url']
        )

        # Step 2. Create an external form fill session
        form_fill_session_api = ExternalFormFillSessionsApi(api_client)
        results = form_fill_session_api.create_external_form_fill_session(
            body=request_body,
            account_id=args["account_id"]
        )
        return results

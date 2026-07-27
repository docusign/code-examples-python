from datetime import datetime as dt, timezone
from docusign_rooms import FieldDataForCreate, RolesApi, RoomsApi, RoomForCreate, RoomTemplatesApi
from flask import session, request

from ..utils import create_rooms_api_client


class Eg002CreateRoomWithTemplateController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "room_name": request.form.get("room_name"),
            "template_id": request.form.get("template_id"),
        }

    @staticmethod
    def get_templates(args):
        """
        1. Create an API client with headers
        2. Get room templates
        """
        # Step 1. Create an API client with headers
        api_client = create_rooms_api_client(access_token=args["access_token"])

        # Step 2. Get room templates
        #ds-snippet-start:Rooms2Step3
        room_templates_api = RoomTemplatesApi(api_client)
        (templates, status, headers) = room_templates_api.get_room_templates_with_http_info(account_id=args["account_id"])

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms2Step3

        return templates.room_templates

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get Default Admin role id
        3. Create RoomForCreate object
        4. Post the room using SDK
        """
        # Step 1. Create an API client with headers
        #ds-snippet-start:Rooms2Step2
        api_client = create_rooms_api_client(access_token=args["access_token"])
        #ds-snippet-end:Rooms2Step2

        # Step 2. Get Default Admin role id
        #ds-snippet-start:Rooms2Step4
        roles_api = RolesApi(api_client)
        (roles, status, headers) = roles_api.get_roles_with_http_info(account_id=args["account_id"])

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        role_id = [role.role_id for role in roles.roles if role.is_default_for_admin][0]

        # Step 3. Create RoomForCreate object
        room = RoomForCreate(
            name=args["room_name"],
            role_id=role_id,
            template_id=args['template_id'],
            field_data=FieldDataForCreate(
                data={
                    'address1': '123 EZ Street',
                    'city': 'Galaxian',
                    'state': 'US-HI',
                    'postalCode': '11111',
                }
            )
        )
        #ds-snippet-end:Rooms2Step4

        # Step 4. Create the room using a POST API call.
        #ds-snippet-start:Rooms2Step5
        rooms_api = RoomsApi(api_client)
        (response, status, headers) = rooms_api.create_room_with_http_info(
            body=room,
            account_id=args["account_id"],
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:Rooms2Step5

        return response

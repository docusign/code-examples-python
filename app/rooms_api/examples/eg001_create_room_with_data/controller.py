from docusign_rooms import ApiClient, RoomsApi, RolesApi, RoomForCreate, FieldDataForCreate
from flask import session, request


class Eg001Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "room_name": request.form.get("room_name"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get Default Admin role id
        3. Create RoomForCreate object
        4. Post the room using SDK
        """
        # Step 1. Create an API client with headers
        api_client = ApiClient(host="https://demo.rooms.docusign.com/restapi")
        api_client.set_default_header(header_name="Authorization",
                                      header_value=f"Bearer {args['access_token']}")

        # Step 2. Get Default Admin role id
        roles_api = RolesApi(api_client)
        roles = roles_api.get_roles(account_id=args["account_id"])
        role_id = [role.role_id for role in roles.roles if role.is_default_for_admin][0]

        # Step 3. Create RoomForCreate object
        room = RoomForCreate(
            name=args["room_name"],
            role_id=role_id,
            transaction_side_id="listbuy",
            field_data=FieldDataForCreate(
                data={
                    'address1': '123 EZ Street',
                    'address2': 'unit 10',
                    'city': 'Galaxian',
                    'state': 'US-HI',
                    'postalCode': '88888',
                    'companyRoomStatus': '5',
                    'comments': '''Lorem ipsum dolor sit amet, consectetur adipiscin'''
                }
            )
        )

        # Step 4. Post the room using SDK
        rooms_api = RoomsApi(api_client)
        response = rooms_api.create_room(room_for_create=room,
                                         account_id=args["account_id"])
        return response

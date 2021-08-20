from docusign_admin.apis import UsersApi
from flask import session

from app.admin.utils import create_admin_api_client
from app.consts import pattern
from app.ds_config import DS_CONFIG


class Eg001Controller:

    @staticmethod
    def get_args(request):
        """
        Get request and session arguments
        """

        return {
            'first_name': pattern.sub("", request.form.get("first_name")),
            'last_name': pattern.sub("", request.form.get("last_name")),
            'user_email': pattern.sub("", request.form.get("user_email")),
            'profile_id': pattern.sub("", request.form.get("profile_id")),
            'group_id': pattern.sub("", request.form.get("group_id")),
            'activate_membership': bool(request.form.get("activate_membership"))
        }

    @staticmethod
    def worker(args):
        """
        1. Create the API client object
        2. Create the user API request object
        3. Create a request body for the create_user method
        4. Creates a user using a method from the user API
        """

        # 1. Create the API client object 
        api_client = create_admin_api_client(
            access_token=session["ds_access_token"]
        )

        # 2. Create the user API request object
        user_api = UsersApi(api_client=api_client)

        # 3. Create a request body for the create_user method 
        request_body = {
            "user_name": f"{args['first_name']} {args['last_name']}",
            "first_name": args['first_name'],
            "last_name": args['last_name'],
            "email": args['user_email'],
            "auto_activate_memberships": args['activate_membership'],
            "accounts": [
                {
                    "id": session["ds_account_id"],
                    "permission_profile": {
                        "id": args['profile_id'],
                    },
                    "groups": [
                        {
                            "id": args['group_id'],
                        }
                    ]
                }
            ]
        }

        # 4. Creates a user using a method from the user API
        response = user_api.create_user(
            DS_CONFIG["organization_id"],
            request_body
        )
        return response

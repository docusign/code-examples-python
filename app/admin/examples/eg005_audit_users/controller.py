from docusign_admin import ApiClient, UsersApi
from flask import session, json

from ....ds_config import DS_CONFIG
from app.admin.utils import get_organization_id
import datetime

class Eg005Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        organization_id = get_organization_id()
        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
            "organization_id": organization_id, # Represents your {ORGANIZATION_ID}
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get your monitor data via SDK
        """

        access_token = args["access_token"]
        account_id = args["account_id"]
        org_id = args["organization_id"]

        # Create an API client with headers
        # Step 2 start
        api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
        api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )
        # Step 2 end

        #Step 3 start
        today = datetime.datetime.now()
        ten_days_ago = today - (datetime.timedelta(days = 10))
        last_modified_since = ten_days_ago.strftime('%Y-%m-%d')

        users_api = UsersApi(api_client=api_client)
        users = users_api.get_users(
            organization_id=org_id,
            account_id=account_id, 
            last_modified_since=last_modified_since)
        # Step 3 end

        # Step 4 start
        modified_users = users.users
        emails = []
        for user in modified_users:
            dict_user = user.to_dict()
            emails.append(dict_user["email"])
        # Step 4 end

        # Step 5 start
        profile_list = []
        for email in emails:
            profile = users_api.get_user_profiles(organization_id=org_id, email=email)
            profile_list.append(profile.to_dict())

        results = {"Modified users": profile_list}
        # Step 5 end

        return results

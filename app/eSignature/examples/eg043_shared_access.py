from flask import session, request
from docusign_esign import EnvelopesApi, UsersApi, AccountsApi, NewUsersDefinition, UserInformation,\
    UserAuthorizationCreateRequest, AuthorizationUser
from datetime import datetime, timedelta

from ...consts import pattern
from ...ds_config import DS_JWT
from ...docusign import create_api_client


class Eg043SharedAccessController:
    @classmethod
    def create_agent(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        users_api = UsersApi(api_client)

        return users_api.create(args["account_id"], new_users_definition=cls.new_users_definition(args))

    @classmethod
    def create_authorization(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        accounts_api = AccountsApi(api_client)

        return accounts_api.create_user_authorization(
            args["account_id"],
            args["user_id"],
            user_authorization_create_request=cls.user_authorization_request(args)
        )

    @classmethod
    def new_users_definition(cls, args):
        agent = UserInformation(
            user_name=args["user_name"],
            email=args["email"],
            activation_access_code=args["activation"]
        )
        return NewUsersDefinition(new_users=[agent])

    @classmethod
    def user_authorization_request(cls, args):
        return UserAuthorizationCreateRequest(
            agent_user=AuthorizationUser(
                account_id=args["account_id"],
                user_id=args["agent_user_id"]
            ),
            permission="manage"
        )

    @classmethod
    def get_envelopes(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        api_client.set_default_header("X-DocuSign-Act-On-Behalf", args["user_id"])
        envelopes_api = EnvelopesApi(api_client)

        from_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        return envelopes_api.list_status_changes(account_id=args["account_id"], from_date=from_date)

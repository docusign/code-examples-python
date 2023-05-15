import json

from docusign_esign import EnvelopesApi, UsersApi, AccountsApi, NewUsersDefinition, UserInformation, \
    UserAuthorizationCreateRequest, AuthorizationUser, ApiException
from datetime import datetime, timedelta

from ...docusign import create_api_client


class Eg043SharedAccessController:
    @classmethod
    def create_agent(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        users_api = UsersApi(api_client)

        try:
            users = users_api.list(args["account_id"], email=args["email"], status="Active")
            if int(users.result_set_size) > 0:
                return users.users[0]

        except ApiException as err:
            error_body_json = err and hasattr(err, "body") and err.body
            error_body = json.loads(error_body_json)
            error_code = error_body and "errorCode" in error_body and error_body["errorCode"]

            if error_code != "USER_NOT_FOUND":
                raise err

        new_users = users_api.create(args["account_id"], new_users_definition=cls.new_users_definition(args))
        return new_users.new_users[0]

    @classmethod
    def create_authorization(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        accounts_api = AccountsApi(api_client)

        authorizations = accounts_api.get_agent_user_authorizations(
            args["account_id"],
            args["agent_user_id"],
            permissions="manage"
        )
        if int(authorizations.result_set_size) > 0:
            return

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

        from_date = (datetime.utcnow() - timedelta(days=10)).isoformat()
        return envelopes_api.list_status_changes(account_id=args["account_id"], from_date=from_date)

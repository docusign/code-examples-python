import json

from docusign_esign import EnvelopesApi, UsersApi, AccountsApi, NewUsersDefinition, UserInformation, \
    UserAuthorizationCreateRequest, AuthorizationUser, ApiException
from datetime import datetime, timedelta

from ...docusign import create_api_client


class Eg043SharedAccessController:
    @classmethod
    def create_agent(cls, args):
        #ds-snippet-start:eSign43Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign43Step2
        #ds-snippet-start:eSign43Step3
        users_api = UsersApi(api_client)
        #ds-snippet-end:eSign43Step3

        # check if agent already exists
        try:
            users = users_api.list(args["account_id"], email=args["email"], status="Active")
            if int(users.result_set_size) > 0:
                return users.users[0]

        except ApiException as err:
            error_body_json = err and hasattr(err, "body") and err.body
            error_body = json.loads(error_body_json)
            error_code = error_body and "errorCode" in error_body and error_body["errorCode"]

            user_not_found_error_codes = ["USER_NOT_FOUND", "USER_LACKS_MEMBERSHIP"]
            if error_code not in user_not_found_error_codes:
                raise err

        # create new agent
        #ds-snippet-start:eSign43Step3
        new_users = users_api.create(args["account_id"], new_users_definition=cls.new_users_definition(args))
        return new_users.new_users[0]
        #ds-snippet-end:eSign43Step3

    #ds-snippet-start:eSign43Step4
    @classmethod
    def create_authorization(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        accounts_api = AccountsApi(api_client)

        # check if authorization with manage permission already exists
        authorizations = accounts_api.get_agent_user_authorizations(
            args["account_id"],
            args["agent_user_id"],
            permissions="manage"
        )
        if int(authorizations.result_set_size) > 0:
            return

        # create authorization
        return accounts_api.create_user_authorization(
            args["account_id"],
            args["user_id"],
            user_authorization_create_request=cls.user_authorization_request(args)
        )
        #ds-snippet-end:eSign43Step4

    #ds-snippet-start:eSign43Step3
    @classmethod
    def new_users_definition(cls, args):
        agent = UserInformation(
            user_name=args["user_name"],
            email=args["email"],
            activation_access_code=args["activation"]
        )
        return NewUsersDefinition(new_users=[agent])
    #ds-snippet-end:eSign43Step3

    @classmethod
    def user_authorization_request(cls, args):
        return UserAuthorizationCreateRequest(
            agent_user=AuthorizationUser(
                account_id=args["account_id"],
                user_id=args["agent_user_id"]
            ),
            permission="manage"
        )

    #ds-snippet-start:eSign43Step5
    @classmethod
    def get_envelopes(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        api_client.set_default_header("X-DocuSign-Act-On-Behalf", args["user_id"])
        envelopes_api = EnvelopesApi(api_client)

        from_date = (datetime.utcnow() - timedelta(days=10)).isoformat()
        return envelopes_api.list_status_changes(account_id=args["account_id"], from_date=from_date)
    #ds-snippet-end:eSign43Step5

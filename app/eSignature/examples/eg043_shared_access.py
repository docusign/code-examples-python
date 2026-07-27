import json

from docusign_esign import EnvelopesApi, UsersApi, AccountsApi, NewUsersDefinition, UserInformation, \
    UserAuthorizationCreateRequest, AuthorizationUser, ApiException
from datetime import datetime as dt, timedelta, timezone

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
            (users, status, headers) = users_api.list_with_http_info(args["account_id"], email=args["email"], status="Active")

            remaining = headers.get("X-RateLimit-Remaining")
            reset = headers.get("X-RateLimit-Reset")

            if remaining is not None and reset is not None:
                reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
                print(f"API calls remaining: {remaining}")
                print(f"Next Reset: {reset_date}")

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
        (new_users, status, headers) = users_api.create_with_http_info(args["account_id"], new_users_definition=cls.new_users_definition(args))

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        return new_users.new_users[0]
        #ds-snippet-end:eSign43Step3

    #ds-snippet-start:eSign43Step4
    @classmethod
    def create_authorization(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        accounts_api = AccountsApi(api_client)

        # check if authorization with manage permission already exists
        (authorizations, status, headers) = accounts_api.get_agent_user_authorizations_with_http_info(
            args["account_id"],
            args["agent_user_id"],
            permissions="manage"
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        if int(authorizations.result_set_size) > 0:
            return

        # create authorization
        (authorization, status, headers) = accounts_api.create_user_authorization_with_http_info(
            args["account_id"],
            args["user_id"],
            user_authorization_create_request=cls.user_authorization_request(args)
        )

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:eSign43Step4

        return authorization

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

        from_date = (dt.utcnow() - timedelta(days=10)).isoformat()
        (envelopes, status, headers) = envelopes_api.list_status_changes_with_http_info(account_id=args["account_id"], from_date=from_date)

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        return envelopes
    #ds-snippet-end:eSign43Step5

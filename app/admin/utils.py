from docusign_orgadmin import ApiClient, AccountsApi
from flask import session

from ..ds_config import DS_CONFIG


def get_organization_id():
    account_id = session["ds_account_id"]
    access_token = session["ds_access_token"]
    api_client = ApiClient(host=DS_CONFIG["admin_api_client_host"])
    api_client.set_default_header(
            header_name="Authorization",
            header_value=f"Bearer {access_token}"
        )

    accounts_api = AccountsApi(api_client)
    organizations = accounts_api.get_organizations()
    org_dict = organizations.to_dict()
    first_org = org_dict["organizations"][0]
    org_id = first_org["id"]

    return org_id
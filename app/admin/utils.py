import docusign_admin as docusign

from app.ds_config import DS_CONFIG


def create_admin_api_client(access_token):
    """Create API client and construct API headers"""

    # return api_client
    api_client = docusign.ApiClient(
        host=DS_CONFIG["admin_api_client_host"],
        header_name="Authorization",
        header_value=f"Bearer {access_token}"
    )
    return api_client

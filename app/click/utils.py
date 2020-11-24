from docusign_click import ApiClient


def create_click_api_client(access_token):
    """Create Click API client and construct API headers"""
    api_client = ApiClient(host="https://demo.docusign.net/clickapi")
    api_client.set_default_header(
        header_name="Authorization",
        header_value=f"Bearer {access_token}"
    )
    return api_client

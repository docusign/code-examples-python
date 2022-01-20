from docusign_admin import ApiClient
from docusign_admin.apis import BulkExportsApi
from flask import session

from app.admin.utils import create_admin_api_client, get_organization_id
from app.ds_config import DS_CONFIG


class Eg003BulkExportUserDataController:

    @classmethod
    def worker(cls):
        """
        1. Create the export API object
        2. Create a user list export request
        3. Save user_list_export_id in a client session
        4. Returns a list of pending and completed export requests
        """

        organization_id = get_organization_id()

        api_client = create_admin_api_client(
            access_token=session["ds_access_token"]
        )

        # Create the export API object
        export_api = BulkExportsApi(api_client=api_client)

        # Create a user list export request
        # Step 3 start
        response = export_api.create_user_list_export(
            organization_id,
            {
                "type": "organization_memberships_export"
            }
        )
        # Step 3 end

        # Save user_list_export_id in a client session
        session['user_list_export_id'] = response.id

        # Returns a list of pending and completed export requests
        return response

    @classmethod
    def get_csv_user_list(cls):
        """
        Getting the csv file of the current list of users:
        1. Create the export API object
        2. Getting the user list export response
        3. Trying to get the user list export id
        4. Create the API client object
        5. Add headers to the API client object and the desired URL
        6. Getting a response containing a csv file
        7. Returns the csv file
        """

        organization_id = get_organization_id()

        # Step 2 start
        api_client = create_admin_api_client(
            access_token=session["ds_access_token"]
        )

        # Create the export API object
        export_api = BulkExportsApi(api_client=api_client)
        # Step 2 end

        # Getting the user list export response
        # Step 4 start
        response = export_api.get_user_list_export(
            organization_id,
            session['user_list_export_id']
        )
        # Step 4 end

        # Trying to get the user list export id
        try: 
            obj_id = response.results[0].id
        except TypeError: 
            return None 

        # Create the API client object
        # Step 5 start
        api_client = ApiClient()

        # Add headers to the API client object and the desired URL
        headers = {"Authorization": "Bearer " + session["ds_access_token"]}
        url = (
            "https://demo.docusign.net/restapi/v2/organization_exports/"
            f"{organization_id}/user_list/{obj_id}"
        )

        # Getting a response containing a csv file
        response = api_client.request("GET", url, headers=headers)
        # Step 5 end

        # Returns the csv file
        return response.data.decode("UTF8")

from docusign_monitor import DataSetApi
from flask import session, json

from app.monitor.utils import create_monitor_api_client


class Eg001Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get your monitor data via SDK
        """

        # Step 1. Create an API client with headers
        api_client = create_monitor_api_client(
            access_token=args["access_token"]
        )

        # Step 1 end

        # Step 2. Get your monitor data
        cursor = ""
        result = []
        while True:
            dataset_api = DataSetApi(api_client=api_client)
            response = dataset_api.get_stream_for_dataset(
                data_set_name="monitor",
                version="2.0",
                _preload_content=False,
                cursor=cursor
            )

            data = json.loads(response.data)

            # If the endCursor from the response is the same as the one
            # that you already have,
            # it means that you have reached the end of the records
            if data["endCursor"] == cursor:
                break

            result.extend(data["data"])
            cursor = data["endCursor"]

        # Step 2 end

        return result

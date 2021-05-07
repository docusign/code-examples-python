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

        # Step 2 start

        # Create an API client with headers
        api_client = create_monitor_api_client(
            access_token=args["access_token"]
        )

        # Step 2 end

        #Step 3 start

        dataset_api = DataSetApi(api_client=api_client)

        cursor = ""
        result = []
        while True:
            response = dataset_api.get_stream_for_dataset(
                data_set_name="monitor",
                version="2.0",
                cursor=cursor
            )

            # If the endCursor from the response is the same as the one
            # that you already have,
            # it means that you have reached the end of the records
            if response["endCursor"] == cursor:
                break

            result.extend([response])
            cursor = response["endCursor"]

        # Step 3 end

        return result

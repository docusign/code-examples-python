from docusign_monitor import DataSetApi
from flask import session

from app.monitor.utils import create_monitor_api_client

class Eg001GetMonitoringDataController:
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
        # Create an API client with headers
        #ds-snippet-start:Monitor1Step2
        api_client = create_monitor_api_client(
            access_token=args["access_token"]
        )
        #ds-snippet-end:Monitor1Step2 
        #ds-snippet-start:Monitor1Step3
        dataset_api = DataSetApi(api_client=api_client)

        cursor_value = '2024-01-01T00:00:00Z'
        limit = 2000
        function_results = []
        complete = False

        while not complete:
            cursored_results = dataset_api.get_stream(
                data_set_name="monitor",
                version="2.0",
                limit=limit,
                cursor=cursor_value
            )
            end_cursor = cursored_results.end_cursor

            if end_cursor == cursor_value:
                complete = True
            else:
                cursor_value = end_cursor
                function_results.append(cursored_results.data)

        #ds-snippet-end:Monitor1Step3
        return function_results

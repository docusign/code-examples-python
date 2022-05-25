from docusign_monitor import DataSetApi
from flask import session, request
from datetime import datetime

from app.monitor.utils import create_monitor_api_client


class Eg002PostWebQueryController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"], # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"], # Represents your {ACCESS_TOKEN}
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date")
        }

    @classmethod
    def worker(cls, args):
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

        # Step 4 start
        dataset_api = DataSetApi(api_client=api_client)
        result = dataset_api.post_web_query(
            data_set_name="monitor",
            version="2.0",
            web_query=cls.get_query(args))
        # Step 4 end


        return result

    # Step 3 start
    @classmethod
    def get_query(cls, args):
        return {
            "filters": [
                {
                    "FilterName": "Time",
                    "BeginTime": datetime.strptime(args['start_date'], "%Y-%m-%d"),
                    "EndTime": datetime.strptime(args['end_date'], "%Y-%m-%d")
                },
                {
                    "FilterName": "Has",
                    "ColumnName": "AccountId",
                    "Value": args["account_id"]
                }
            ],
            "aggregations": [
                {
                    "aggregationName": "Raw",
                    "limit": "1",
                    "orderby": [
                        "Timestamp, desc"
                    ]
                }
            ]
        }

    # Step 3 end

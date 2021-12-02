from datetime import datetime, timedelta

from docusign_esign import EnvelopesApi
from flask import session

from ...docusign import create_api_client


class Eg003ListEnvelopesController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        return {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
        }

    @staticmethod
    def worker(args):
        """
        1. Call the envelope status change method to list the envelopes
           that have changed in the last 10 days
        """
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)

        # The Envelopes::listStatusChanges method has many options
        # See https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopes/liststatuschanges/

        # The list status changes call requires at least a from_date OR
        # a set of envelopeIds. Here we filter using a from_date.
        # Here we set the from_date to filter envelopes for the last month
        # Use ISO 8601 date format
        # 1. Call the envelope status change method to list the envelopes
        from_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        results = envelope_api.list_status_changes(account_id=args["account_id"], from_date=from_date)

        return results

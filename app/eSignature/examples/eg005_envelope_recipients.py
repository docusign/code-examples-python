from docusign_esign import EnvelopesApi
from flask import session

from ...docusign import create_api_client


class Eg005EnvelopeRecipientsController:
    @staticmethod
    def get_args():
        """
        Get session arguments
        """
        return {
            "account_id": session["ds_account_id"],
            "envelope_id": session["envelope_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
        }

    @staticmethod
    def worker(args):
        """
        1. Call the envelope recipients list method
        """

        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        # 1. Call the envelope recipients list method
        results = envelope_api.list_recipients(account_id=args["account_id"], envelope_id=args["envelope_id"])

        return results

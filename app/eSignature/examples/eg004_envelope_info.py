from docusign_esign import EnvelopesApi
from flask import session

from ...docusign import create_api_client


class Eg004EnvelopeInfoController:
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
        1. Call the envelope get method
        """

        # Exceptions will be caught by the calling function
        #ds-snippet-start:eSign4Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        # Call the envelope get method
        results = envelope_api.get_envelope(account_id=args["account_id"], envelope_id=args["envelope_id"])
        #ds-snippet-end:eSign4Step2
        return results

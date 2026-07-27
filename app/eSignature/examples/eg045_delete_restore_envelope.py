from datetime import datetime as dt, timezone
from docusign_esign import FoldersApi, FoldersRequest

from ...docusign import create_api_client


class Eg045DeleteRestoreEnvelopeController:
    @staticmethod
    def delete_envelope(args):
        #ds-snippet-start:eSign45Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        folders_api = FoldersApi(api_client)
        #ds-snippet-end:eSign45Step2

        #ds-snippet-start:eSign45Step3
        folders_request = FoldersRequest(
            envelope_ids=[args["envelope_id"]]
        )
        #ds-snippet-end:eSign45Step3

        #ds-snippet-start:eSign45Step4
        (results, status, headers) = folders_api.move_envelopes_with_http_info(account_id=args["account_id"], folder_id=args["delete_folder_id"], folders_request=folders_request)

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:eSign45Step4

        return results

    @staticmethod
    def move_envelope_to_folder(args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        folders_api = FoldersApi(api_client)

        #ds-snippet-start:eSign45Step6
        folders_request = FoldersRequest(
            envelope_ids=[args["envelope_id"]],
            from_folder_id=args["from_folder_id"]
        )

        (results, status, headers) = folders_api.move_envelopes_with_http_info(account_id=args["account_id"], folder_id=args["folder_id"], folders_request=folders_request)

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:eSign45Step6

        return results

    @staticmethod
    def get_folders(args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        folders_api = FoldersApi(api_client)

        #ds-snippet-start:eSign45Step5
        (results, status, headers) = folders_api.list_with_http_info(account_id=args["account_id"])

        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")
        #ds-snippet-end:eSign45Step5

        return results

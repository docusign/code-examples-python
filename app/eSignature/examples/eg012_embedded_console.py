from docusign_esign import EnvelopesApi, ConsoleViewRequest
from flask import session, url_for, request

from ...consts import pattern
from ...docusign import create_api_client


class Eg012EmbeddedConsoleController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # Strip anything other than characters listed
        starting_view = pattern.sub("", request.form.get("starting_view"))
        envelope_id = "envelope_id" in session and session["envelope_id"]
        args = {
            "envelope_id": envelope_id,
            "starting_view": starting_view,
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "ds_return_url": url_for("ds.ds_return", _external=True),
        }

        return args

    @staticmethod
    def worker(args):
        """
        This function does the work of returning a URL for the NDSE view
        """

        # Step 1. Create the NDSE view request object
        # Set the url where you want the recipient to go once they are done
        # with the NDSE. It is usually the case that the
        # user will never "finish" with the NDSE.
        # Assume that control will not be passed back to your app.
        #ds-snippet-start:eSign12Step2
        view_request = ConsoleViewRequest(return_url=args["ds_return_url"])
        if args["starting_view"] == "envelope" and args["envelope_id"]:
            view_request.envelope_id = args["envelope_id"]

        # Step 2. Get the console view url
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_console_view(account_id=args["account_id"], console_view_request=view_request)
        url = results.url
        #ds-snippet-end:eSign12Step2
        return {"redirect_url": url}

from docusign_esign import EnvelopesApi, ReturnUrlRequest
from flask import url_for, session, request

from .eg002_signing_via_email import Eg002SigningViaEmailController
from ...consts import pattern, demo_docs_path
from ...docusign import create_api_client


class Eg011EmbeddedSendingController:

    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = pattern.sub("", request.form.get("cc_email"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
        starting_view = pattern.sub("", request.form.get("starting_view"))

        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "cc_email": cc_email,
            "cc_name": cc_name,
            "status": "sent",
        }
        args = {
            "starting_view": starting_view,
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "envelope_args": envelope_args,
            "ds_return_url": url_for("ds.ds_return", _external=True),
        }
        return args

    @staticmethod
    def worker(args,doc_docx_path,doc_pdf_path):
        """
        This function does the work of creating the envelope in
        draft mode and returning a URL for the sender"s view
        """

        # Step 1. Create the envelope with "created" (draft) status
        args["envelope_args"]["status"] = "created"
        # Using worker from example 002
        results = Eg002SigningViaEmailController.worker(args, doc_docx_path, doc_pdf_path)
        envelope_id = results["envelope_id"]

        # Step 2. Create the sender view
        view_request = ReturnUrlRequest(return_url=args["ds_return_url"])
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_sender_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            return_url_request=view_request
        )

        # Switch to Recipient and Documents view if requested by the user
        url = results.url
        if args["starting_view"] == "recipient":
            url = url.replace("send=1", "send=0")

        return {"envelope_id": envelope_id, "redirect_url": url}

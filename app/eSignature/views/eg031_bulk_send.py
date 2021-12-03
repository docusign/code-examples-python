"""Example 031: Send an envelope to multiple recipients"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint
from ..examples.eg031_bulk_send import Eg031BulkSendController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg031"  # reference and url for this example
eg031 = Blueprint("eg031", __name__)

@eg031.route("/eg031", methods=["POST"])
@authenticate(eg=eg)
def bulk_send():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render response
    """

    # 1. Get required arguments
    args = Eg031BulkSendController.get_args()
    try:
        # 2. Call the worker method for bulk sending
        response = Eg031BulkSendController.worker(args)
        queued = response.queued
        app.logger.info(f"The envelope has been sent to multiple recipients.")

        # 3. Render the response
        return render_template("example_done.html",
                               title="Bulk send envelope was successfully performed!",
                               h1="Bulk send envelope was successfully performed!",
                               message=f"""Bulk request queued to {queued} user lists.<br/>"""
                               )

    except ApiException as err:
        return process_error(err)


@eg031.route("/eg031", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg031_bulk_send.html",
        title="Bulk sending envelopes to multiple recipients",
        source_file= "eg031_bulk_send.py",
        source_url=DS_CONFIG["github_example_url"] + "eg031_bulk_send.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )
"""005: List an envelope"s recipients and status"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from .eg005_envelope_recipients import Eg005EnvelopeRecipientsController
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg005"  # reference (and url) for this example
eg005 = Blueprint("eg005", __name__)


@eg005.route("/eg005", methods=["POST"])
@authenticate(eg=eg)
def envelope_recipients():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show recipients
    """

    if "envelope_id" in session:
        # 1. Get required arguments
        args = Eg005EnvelopeRecipientsController.get_args()
        try:
            # 2. Call the worker method
            results = Eg005EnvelopeRecipientsController.worker(args)
        except ApiException as err:
            return process_error(err)
        # 3. Show recipients
        return render_template(
            "example_done.html",
            title="Envelope recipients results",
            h1="List the envelope's recipients and their status",
            message="Results from the EnvelopesRecipients::list method:",
            json=json.dumps(json.dumps(results.to_dict()))
        )
    else:
        return render_template(
            "eg005_envelope_recipients.html",
            title="Envelope recipient information",
            envelope_ok=False,
            source_file=path.basename(path.dirname(__file__)) + "/eg005_envelope_recipients.py",
            source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg005_envelope_recipients.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg005.route("/eg005", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg005_envelope_recipients.html",
        title="Envelope recipient information",
        envelope_ok="envelope_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/eg005_envelope_recipients.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg005_envelope_recipients.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

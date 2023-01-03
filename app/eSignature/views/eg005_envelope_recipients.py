"""005: List an envelope"s recipients and status"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, session

from ..examples.eg005_envelope_recipients import Eg005EnvelopeRecipientsController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 5
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg005 = Blueprint(eg, __name__)


@eg005.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def envelope_recipients():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show recipients
    """
    example = get_example_by_number(session["manifest"], example_number, api)

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
            title=example["ExampleName"],
            message="Results from the EnvelopesRecipients::list method:",
            json=json.dumps(json.dumps(results.to_dict()))
        )
    else:
        return render_template(
            "eSignature/eg005_envelope_recipients.html",
            title=example["ExampleName"],
            example=example,
            envelope_ok=False,
            source_file= "eg005_envelope_recipients.py",
            source_url=DS_CONFIG["github_example_url"] + "eg005_envelope_recipients.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg005.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg005_envelope_recipients.html",
        title=example["ExampleName"],
        example=example,
        envelope_ok="envelope_id" in session,
        source_file= "eg005_envelope_recipients.py",
        source_url=DS_CONFIG["github_example_url"] + "eg005_envelope_recipients.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

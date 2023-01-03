"""Example 031: Send an envelope to multiple recipients"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint, session

from ..examples.eg031_bulk_send import Eg031BulkSendController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 31
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference and url for this example
eg031 = Blueprint(eg, __name__)

@eg031.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def bulk_send():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg031BulkSendController.get_args()
    try:
        # 2. Call the worker method for bulk sending
        response = Eg031BulkSendController.worker(args)
        queued = response.queued
        app.logger.info(f"The envelope has been sent to multiple recipients.")

        # 3. Render the response
        return render_template("example_done.html",
                               title=example["ExampleName"],
                               message=f"""Results from BulkSend:getBulkSendBatchStatus method:<br/>""",
                               json=json.dumps(json.dumps(response.to_dict()))
                               )

    except ApiException as err:
        return process_error(err)


@eg031.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg031_bulk_send.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg031_bulk_send.py",
        source_url=DS_CONFIG["github_example_url"] + "eg031_bulk_send.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )
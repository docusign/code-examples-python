"""004: Get an envelope"s basic information and status"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg004_envelope_info import Eg004EnvelopeInfoController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 4
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg004 = Blueprint(eg, __name__)


@eg004.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def envelope_info():
    """
    1. Get required arguments
    1. Call the worker method
    2. Show envelope info
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    if "envelope_id" in session:
        # 1. Get required arguments
        args = Eg004EnvelopeInfoController.get_args()
        try:
            # 1. Call the worker method
            results = Eg004EnvelopeInfoController.worker(args)
        except ApiException as err:
            return process_error(err)
        # 2.Show envelope info
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message="Results from the Envelopes::get method:",
            json=json.dumps(json.dumps(results.to_dict()))
        )
    else:
        return render_template(
            "eSignature/eg004_envelope_info.html",
            title=example["ExampleName"],
            envelope_ok=False,
            source_file= "eg004_envelope_info.py",
            source_url=DS_CONFIG["github_example_url"] + "eg004_envelope_info.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg004.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg004_envelope_info.html",
        title=example["ExampleName"],
        example=example,
        envelope_ok="envelope_id" in session,
        source_file= "eg004_envelope_info.py",
        source_url=DS_CONFIG["github_example_url"] + "eg004_envelope_info.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

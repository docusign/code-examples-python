"""Example 003: List envelopes in the user"s account"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ..examples.eg003_list_envelopes import Eg003ListEnvelopesController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 3
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg003 = Blueprint(eg, __name__)


@eg003.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def envelope_list():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show envelopes
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg003ListEnvelopesController.get_args()
    try:
        # 1. Call the worker method
        results = Eg003ListEnvelopesController.worker(args)
    except ApiException as err:
        return process_error(err)
    # 3. Show envelopes
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from the Envelopes::listStatusChanges method:",
        json=json.dumps(json.dumps(results.to_dict()))
    )


@eg003.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg003_list_envelopes.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg003_list_envelopes.py",
        source_url=DS_CONFIG["github_example_url"] + "eg003_list_envelopes.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

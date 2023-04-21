""" Example 002: Remote signer, cc, envelope has three documents """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, request

from ..examples.eg042_document_generation import Eg042DocumentGenerationController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import pattern, API_TYPE

example_number = 42
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg042 = Blueprint(eg, __name__)


@eg042.route(f"/{eg}", methods=["POST"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def sign_by_email():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

    # 1. Get required arguments
    args = Eg042DocumentGenerationController.get_args()
    try:
        # 1. Call the worker method
        results = Eg042DocumentGenerationController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 2. Render success response with envelopeId
    example = get_example_by_number(session["manifest"], example_number, api)
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"].format(results.envelope_id)
    )


@eg042.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg042_document_generation.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg042_document_generation.py",
        source_url=DS_CONFIG["github_example_url"] + "eg042_document_generation.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

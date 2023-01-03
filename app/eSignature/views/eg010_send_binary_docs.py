""" Example 010: Send binary docs with multipart mime: Remote signer, cc; the envelope has three documents"""

from os import path

from flask import render_template, Blueprint, session

from ..examples.eg010_send_binary_docs import Eg010SendBinaryDocsController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 10
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg010 = Blueprint(eg, __name__)


@eg010.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def send_bynary_docs():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg010SendBinaryDocsController.get_args()
    # 2. Call the worker method
    results = Eg010SendBinaryDocsController.worker(args)

    if results["status_code"] < 299:
        # 3. Render Success response
        return render_template(
            "example_done.html",
            title="Envelope sent",
            h1="Envelope sent",
            message=f"""The envelope has been created and sent!<br/> Envelope ID {results["results"]["envelopeId"]}."""
        )
    else:
        # Problem!
        error_body = results["results"]
        # we can pull the DocuSign error code and message from the response body
        error_code = error_body and "errorCode" in error_body and error_body["errorCode"]
        error_message = error_body and "message" in error_body and error_body["message"]
        # In production, may want to provide customized error messages and
        # remediation advice to the user.
        return render_template(
            "error.html",
            err=None,
            error_code=error_code,
            error_message=error_message
        )


@eg010.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg010_send_binary_docs.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg010_send_binary_docs.py",
        source_url=DS_CONFIG["github_example_url"] + "eg010_send_binary_docs.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

""" Example 010: Send binary docs with multipart mime: Remote signer, cc; the envelope has three documents"""

from os import path

from flask import render_template, Blueprint

from ..examples.eg010_send_binary_docs import Eg010SendBinaryDocsController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG

eg = "eg010"  # reference (and url) for this example
eg010 = Blueprint("eg010", __name__)


@eg010.route("/eg010", methods=["POST"])
@authenticate(eg=eg)
def send_bynary_docs():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

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


@eg010.route("/eg010", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg010_send_binary_docs.html",
        title="Send binary documents",
        source_file= "eg010_send_binary_docs.py",
        source_url=DS_CONFIG["github_example_url"] + "eg010_send_binary_docs.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

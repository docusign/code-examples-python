""" Example 002: Remote signer, cc, envelope has three documents """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg002_signing_via_email import Eg002SigningViaEmailController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg002"  # reference (and url) for this example
eg002 = Blueprint("eg002", __name__)


@eg002.route("/eg002", methods=["POST"])
@authenticate(eg=eg)
def sign_by_email():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

    # 1. Get required arguments
    args = Eg002SigningViaEmailController.get_args()
    try:
        # 1. Call the worker method
        results = Eg002SigningViaEmailController.worker(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]  # Save for use by other examples which need an envelopeId

    # 2. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title="Envelope sent",
        h1="Envelope sent",
        message=f"The envelope has been created and sent!<br/>Envelope ID {results['envelope_id']}."
    )


@eg002.route("/eg002", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg002_signing_via_email.html",
        title="Signing via email",
        source_file="eg002_signing_via_email.py",
        source_url=DS_CONFIG["github_example_url"] + "eg002_signing_via_email.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

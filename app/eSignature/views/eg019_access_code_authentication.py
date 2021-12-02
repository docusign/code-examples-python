""" Example 019: Access Code Recipient Authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint

from ..examples.eg019_access_code_authentication import Eg019AccessCodeAuthenticationController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg019"  # reference (and url) for this example
eg019 = Blueprint("eg019", __name__)

@eg019.route("/eg019", methods=["POST"])
@authenticate(eg=eg)
def access_code_authentication():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """
    args = Eg019AccessCodeAuthenticationController.get_args()
    try:
        # Step 1: Call the worker method for authenticating with access code
        results = Eg019AccessCodeAuthenticationController.worker(args)
        envelope_id = results.envelope_id

        app.logger.info(f"Envelope was created. EnvelopeId {envelope_id} ")

        return render_template(
            "example_done.html",
            title="Envelope sent",
            h1="Envelope sent",
            message=f"""The envelope has been created and sent!<br/> Envelope ID {envelope_id}."""
        )

    except ApiException as err:
        return process_error(err)


@eg019.route("/eg019", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg019_access_code_authentication.html",
        title="Access-code recipient authentication",
        source_file=path.basename(path.dirname(__file__)) + "/eg019_access_code_authentication.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg019_access_code_authentication.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

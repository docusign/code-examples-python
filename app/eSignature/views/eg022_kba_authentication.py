""" Example 022: Knowledge Based authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint

from ..examples.eg022_kba_authentication import Eg022KBAAuthenticationController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg022"  # reference (and url) for this example
eg022 = Blueprint("eg022", __name__)


@eg022.route("/eg022", methods=["POST"])
@authenticate(eg=eg)
def kba_authentication():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    # 1. Get required arguments
    args = Eg022KBAAuthenticationController.get_args()
    try:
        # Step 2: Call the worker method for kba
        results = Eg022KBAAuthenticationController.worker(args)
        envelope_id = results.envelope_id
        app.logger.info(f"Envelope was created. EnvelopeId {envelope_id} ")

        # 3. Render success response
        return render_template(
            "example_done.html",
            title="Envelope sent",
            h1="Envelope sent",
            message=f"""The envelope has been created and sent!<br/> Envelope ID {envelope_id}."""
        )

    except ApiException as err:
        return process_error(err)


@eg022.route("/eg022", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""
    return render_template(
        "eg022_kba_authentication.html",
        title="Kba recipient authentication",
        source_file= "eg022_kba_authentication.py",
        source_url=DS_CONFIG["github_example_url"] + "eg022_kba_authentication.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

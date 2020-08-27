""" Example 020: Sms Recipient Authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint

from .controller import Eg020Controller
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg020"  # reference (and url) for this example
eg020 = Blueprint("eg020", __name__)


@eg020.route("/eg020", methods=["POST"])
@authenticate(eg=eg)
def sms_authentication():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    # 1. Get required arguments
    args = Eg020Controller.get_args()
    try:
        # Step 2: Call the worker method for sms authenticating
        results = Eg020Controller.worker(args)
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


@eg020.route("/eg020", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg020_sms_authentication.html",
        title="SMS recipient authentication",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

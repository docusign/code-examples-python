""" Example 020: Recipient Phone Authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint, session

from .eg020_phone_authentication import Eg020PhoneAuthenticationController
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg020"  # reference (and url) for this example
eg020 = Blueprint("eg020", __name__)


@eg020.route("/eg020", methods=["POST"])
@authenticate(eg=eg)
def phone_authentication():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    # 1. Get required arguments
    args = Eg020PhoneAuthenticationController.get_args()
    try:
        # Step 2: Call the worker method for authenticating with phone
        results = Eg020PhoneAuthenticationController.worker(args)
        envelope_id = results.envelope_id
        app.logger.info(f"Envelope was created. EnvelopeId {envelope_id} ")

        # 3. Render success response
        return render_template(
            "example_done.html",
            title="Require Phone Authentication for a Recipient",
            h1="Require Phone Authentication for a Recipient",
            message=f"""The envelope has been created and sent!<br/> Envelope ID {envelope_id}."""
        )

    except ApiException as err:
        return process_error(err)


@eg020.route("/eg020", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    args = {
        "account_id": session["ds_account_id"],  # represent your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # represent your {ACCESS_TOKEN}
    }

    workflow_id = Eg020PhoneAuthenticationController.get_workflow(args)

    return render_template(
        "eg020_phone_authentication.html",
        title="Requiring phone authentication for a Recipient",
        source_file=path.basename(path.dirname(__file__)) + "/eg020_phone_authentication.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg020_phone_authentication.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"],
        workflow_id = workflow_id
    )

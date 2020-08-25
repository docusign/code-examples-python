""" Example 021: Recipient Phone Authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint

from .controller import Eg021Controller
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg021"  # reference (and url) for this example
eg021 = Blueprint("eg021", __name__)


@eg021.route("/eg021", methods=["POST"])
@authenticate(eg=eg)
def phone_authentication():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    # 1. Get required arguments
    args = Eg021Controller.get_args()
    try:
        # Step 2: Call the worker method for authenticating with phone
        results = Eg021Controller.worker(args)
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


@eg021.route("/eg021", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg021_phone_authentication.html",
        title="Phone recipient authentication",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

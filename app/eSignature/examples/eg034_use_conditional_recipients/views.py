""" Example 034: Creating an envelope where the workflow is routed
to different recipients based on the value of a transaction """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from .controller import Eg034Controller
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg034"  # reference (and url) for this example
eg034 = Blueprint("eg034", __name__)


@eg034.route("/eg034", methods=["POST"])
@authenticate(eg=eg)
def use_conditional_recipients():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

    # 1. Get required arguments
    args = Eg034Controller.get_args()
    try:
        # 1. Call the worker method
        results = Eg034Controller.worker(args)
    except ApiException as err:
        return process_error(err)

    # 2. Render success response with envelopeId
    return render_template(
            "example_done.html",
            envelope_ok=True,
            title="Use conditional recipients",
            h1="Use conditional recipients",
            message=f"Envelope ID {results['envelope_id']} with the conditional"
                    f" routing criteria has been created and sent to the first recipient!"
        )


@eg034.route("/eg034", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg034_use_conditional_recipients.html",
        title="Using conditional recipients",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer1_name=DS_CONFIG["signer_name"],
        signer1_email=DS_CONFIG["signer_email"]
    )

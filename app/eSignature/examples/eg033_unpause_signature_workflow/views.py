""" Example 033: Resuming an envelope workflow that has been paused """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from .controller import Eg033Controller
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg033"  # Reference (and URL) for this example
eg033 = Blueprint("eg033", __name__)


@eg033.route("/eg033", methods=["POST"])
@authenticate(eg=eg)
def unpause_signature_workflow():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

    # 1. Get required arguments
    args = Eg033Controller.get_args()
    try:
        # 1. Call the worker method
        results = Eg033Controller.worker(args)
    except ApiException as err:
        return process_error(err)

    # 2. Render success response with envelopeId
    return render_template(
            "example_done.html",
            envelope_ok=True,
            title="Envelope unpaused",
            h1="Envelope unpaused",
            message=f"The envelope workflow has been resumed and the envelope "
                    f"has been sent to a second recipient!<br/>"
                    f"Envelope ID {results['envelope_id']}."
        )


@eg033.route("/eg033", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg033_unpause_signature_workflow.html",
        title="Unpausing a signature workflow",
        envelope_ok="paused_envelope_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

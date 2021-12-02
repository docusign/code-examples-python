"""011: Embedded sending: Remote signer, cc, envelope has three documents"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint

from ..examples.eg011_embedded_sending import Eg011EmbeddedSendingController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg011"  # reference (and url) for this example
eg011 = Blueprint("eg011", __name__)


@eg011.route("/eg011", methods=["POST"])
@authenticate(eg=eg)
def embedded_sending():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect user to NDSE view
    """

    # 1. Get required arguments
    args = Eg011EmbeddedSendingController.get_args()
    try:
        # 2. Call the worker method
        results = Eg011EmbeddedSendingController.worker(args)
    except ApiException as err:
        return process_error(err)

    # Redirect the user to the NDSE view
    # Don"t use an iFrame!
    # State can be stored/recovered using the framework"s session or a
    # query parameter on the returnUrl (see the makeRecipientViewRequest method)
    return redirect(results["redirect_url"])


@eg011.route("/eg011", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg011_embedded_sending.html",
        title="Embedded Sending",
        source_file=path.basename(path.dirname(__file__)) + "/eg011_embedded_sending.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg011_embedded_sending.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

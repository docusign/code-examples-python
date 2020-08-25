"""Example 001: Embedded Signing Ceremony"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint

from .controller import Eg001Controller
from ..docusign import authenticate
from ..ds_config import DS_CONFIG
from ..error_handlers import process_error

eg = "eg001"  # reference (and url) for this example
eg001 = Blueprint("eg001", __name__)


@eg001.route("/eg001", methods=["POST"])
@authenticate(eg=eg)
def embedded_signing():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect the user to the signing ceremony
    """
    try:
        # 1. Get required arguments
        args = Eg001Controller.get_args()
        # 2. Call the worker method
        results = Eg001Controller.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Redirect the user to the Signing Ceremony
    # Don"t use an iFrame!
    # State can be stored/recovered using the framework"s session or a
    # query parameter on the returnUrl (see the makeRecipientViewRequest method)
    return redirect(results["redirect_url"])


@eg001.route("/eg001", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg001_embedded_signing.html",
        title="Embedded Signing Ceremony",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

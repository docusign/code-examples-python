"""Example 038: Responsive signing"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint

from ..examples.eg038_responsive_signing import Eg038ResponsiveSigning
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg038"  # reference (and url) for this example
eg038 = Blueprint("eg038", __name__)


@eg038.route("/eg038", methods=["POST"])
@authenticate(eg=eg)
def embedded_signing():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect the user to the embedded signing
    """
    try:
        # 1. Get required arguments
        args = Eg038ResponsiveSigning.get_args()
        # 2. Call the worker method
        results = Eg038ResponsiveSigning.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Redirect the user to the embedded signing
    # Don"t use an iFrame!
    # State can be stored/recovered using the framework"s session or a
    # query parameter on the returnUrl (see the makeRecipientViewRequest method)
    return redirect(results["redirect_url"])


@eg038.route("/eg038", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg038_responsive_signing.html",
        title="Responsive signing",
        source_file= "eg038_responsive_signing.py",
        source_url=DS_CONFIG["github_example_url"] + "eg038_responsive_signing.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

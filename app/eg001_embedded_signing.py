"""Example 001: Use embedded signing"""

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint, current_app as app, session, url_for

from .eSignature.examples.eg001_embedded_signing import Eg001EmbeddedSigningController
from .eSignature.examples.eg041_cfr_embedded_signing import Eg041CFREmbeddedSigningController
from .docusign import authenticate, ensure_manifest, get_example_by_number
from .ds_config import DS_CONFIG
from .error_handlers import process_error
from .consts import API_TYPE
from .docusign.utils import is_cfr

example_number = 1
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg001 = Blueprint(eg, __name__)


@eg001.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def embedded_signing():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect the user to the embedded signing
    """
    try:
        # 1. Get required arguments
        args = Eg001EmbeddedSigningController.get_args()
        # 2. Call the worker method
        results = Eg001EmbeddedSigningController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Redirect the user to the embedded signing
    # Don"t use an iFrame!
    # State can be stored/recovered using the framework"s session or a
    # query parameter on the returnUrl (see the makeRecipientViewRequest method)
    return redirect(results["redirect_url"])


@eg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    # Check if account is a CFR Part 11 account and redirect accordingly for Quickstart
    cfr_status = is_cfr(session["ds_access_token"], session["ds_account_id"], session["ds_base_path"])
    if cfr_status == "enabled":
        if DS_CONFIG["quickstart"] == "true":
            return redirect(url_for("eg041.get_view"))
        else:
            return render_template("cfr_error.html", title="Error")

    return render_template(
        "eg001_embedded_signing.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg001_embedded_signing.py",
        source_url=DS_CONFIG["github_example_url"] + "eg001_embedded_signing.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

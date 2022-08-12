""" Example 039: In Person Signer """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint, request

from ..examples.eg039_in_person_signer import Eg039InPersonSigner
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import pattern

eg = "eg039"  # reference (and url) for this example
eg039 = Blueprint("eg039", __name__)

@eg039.route("/eg039", methods=["POST"])
@authenticate(eg=eg)
def in_person_signer():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

    # 1. Get required arguments
    args = Eg039InPersonSigner.get_args()
    try:
        # 1. Call the worker method
        results = Eg039InPersonSigner.worker(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]  # Save for use by other examples which need an envelopeId

    # 2. Redirect to in person signing session
    return redirect(results["redirect_url"])


@eg039.route("/eg039", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg039_in_person_signer.html",
        title="Signing via email",
        source_file="eg039_in_person_signer.py",
        source_url=DS_CONFIG["github_example_url"] + "eg039_in_person_signer.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
    )

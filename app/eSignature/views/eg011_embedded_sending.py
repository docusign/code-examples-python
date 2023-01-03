"""011: Embedded sending: Remote signer, cc, envelope has three documents"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint, session

from ..examples.eg011_embedded_sending import Eg011EmbeddedSendingController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 11
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg011 = Blueprint(eg, __name__)


@eg011.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
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
        results = Eg011EmbeddedSendingController.worker(args, DS_CONFIG["doc_docx"], DS_CONFIG["doc_pdf"])
    except ApiException as err:
        return process_error(err)

    # Redirect the user to the NDSE view
    # Don"t use an iFrame!
    # State can be stored/recovered using the framework"s session or a
    # query parameter on the returnUrl (see the makeRecipientViewRequest method)
    return redirect(results["redirect_url"])


@eg011.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg011_embedded_sending.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg011_embedded_sending.py",
        source_url=DS_CONFIG["github_example_url"] + "eg011_embedded_sending.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

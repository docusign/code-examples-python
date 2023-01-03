"""012: Embedded console"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint

from ..examples.eg012_embedded_console import Eg012EmbeddedConsoleController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 12
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg012 = Blueprint(eg, __name__)


@eg012.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def embedded_console():
    """
    1. Get required args
    2. Call the worker method
    3. Redirect user to NDSE view
    """

    # 1. Get required args
    args = Eg012EmbeddedConsoleController.get_args()
    try:
        # 2. Call the worker method
        results = Eg012EmbeddedConsoleController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Redirect the user to the NDSE view
    # Don"t use an iFrame!
    # State can be stored/recovered using the framework"s session
    return redirect(results["redirect_url"])


@eg012.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    envelope_id = "envelope_id" in session and session["envelope_id"]
    return render_template(
        "eSignature/eg012_embedded_console.html",
        title=example["ExampleName"],
        example=example,
        envelope_ok=envelope_id,
        source_file= "eg012_embedded_console.py",
        source_url=DS_CONFIG["github_example_url"] + "eg012_embedded_console.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

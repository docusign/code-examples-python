"""012: Embedded console"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint

from ..examples.eg012_embedded_console import Eg012EmbeddedConsoleController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg012"  # reference (and url) for this example
eg012 = Blueprint("eg012", __name__)


@eg012.route("/eg012", methods=["POST"])
@authenticate(eg=eg)
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


@eg012.route("/eg012", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    envelope_id = "envelope_id" in session and session["envelope_id"]
    return render_template(
        "eg012_embedded_console.html",
        title="Embedded Console",
        envelope_ok=envelope_id,
        source_file= "eg012_embedded_console.py",
        source_url=DS_CONFIG["github_example_url"] + "eg012_embedded_console.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

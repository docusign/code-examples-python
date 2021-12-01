"""Example 016: Set Tab Values"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint

from .eg016_set_tab_values import Eg016SetTabValuesController
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg016"  # Reference (and URL) for this example
eg016 = Blueprint("eg016", __name__)


# the signer? See the "authenticationMethod" definition
# https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopeviews/createrecipient/


@eg016.route("/eg016", methods=["POST"])
@authenticate(eg=eg)
def set_tab_values():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect the user to the embedded signing
    """

    # 1. Get required arguments
    args = Eg016SetTabValuesController.get_args()

    try:
        # 2. Call the worker method for setting tab values
        results = Eg016SetTabValuesController.worker(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]  # Save for use by other examples
    # that need an envelope ID
    # 3. Redirect the user to the embedded signing
    # Don"t use an iframe!
    # State can be stored/recovered using the framework"s session or a
    # query parameter on the return URL (see the makeRecipientViewRequest method)
    return redirect(results["redirect_url"])


@eg016.route("/eg016", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg016_set_tab_values.html",
        title="SetTabValues",
        source_file=path.basename(path.dirname(__file__)) + "/eg016_set_tab_values.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg016_set_tab_values.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

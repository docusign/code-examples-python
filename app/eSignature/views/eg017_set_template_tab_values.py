"""Example 017: Set Template Tab Values"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint

from .eg017_set_template_tab_values import Eg017SetTemplateTabValuesController
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg017"  # reference (and url) for this example
eg017 = Blueprint("eg017", __name__)


# the signer? See the "authenticationMethod" definition
# https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopeviews/createrecipient/


@eg017.route("/eg017", methods=["POST"])
@authenticate(eg=eg)
def set_template_tab_values():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect the user to the embedded signing
    """

    # 1. Get required arguments
    args = Eg017SetTemplateTabValuesController.get_args()

    try:
        # 2. Call the worker method for setting template tab values
        results = Eg017SetTemplateTabValuesController.worker(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]  # Save for use by other examples
    # which need an envelopeId
    # 3. Redirect the user to the embedded signing
    # Don"t use an iFrame!
    # State can be stored/recovered using the framework"s session or a
    # query parameter on the returnUrl (see the makeRecipientViewRequest method)
    return redirect(results["redirect_url"])


@eg017.route("/eg017", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg017_set_template_tab_values.html",
        title="SetTemplateTabValues",
        template_ok="template_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/eg017_set_template_tab_values.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg017_set_template_tab_values.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

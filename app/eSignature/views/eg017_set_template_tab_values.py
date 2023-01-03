"""Example 017: Set Template Tab Values"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint

from ..examples.eg017_set_template_tab_values import Eg017SetTemplateTabValuesController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 17
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg017 = Blueprint(eg, __name__)


# the signer? See the "authenticationMethod" definition
# https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopeviews/createrecipient/


@eg017.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
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


@eg017.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg017_set_template_tab_values.html",
        title=example["ExampleName"],
        example=example,
        template_ok="template_id" in session,
        source_file= "eg017_set_template_tab_values.py",
        source_url=DS_CONFIG["github_example_url"] + "eg017_set_template_tab_values.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

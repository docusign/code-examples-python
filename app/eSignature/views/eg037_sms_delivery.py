""" Example 037: SMS Delivery """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg037_sms_delivery import Eg037SMSDeliveryController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...docusign.utils import is_cfr
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 37
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg037 = Blueprint(eg, __name__)


@eg037.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def sign_by_email():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg037SMSDeliveryController.get_args()
    try:
        # 1. Call the worker method
        results = Eg037SMSDeliveryController.worker(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]  # Save for use by other examples which need an envelopeId

    # 2. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=f"The envelope has been created and sent!<br/>Envelope ID {results['envelope_id']}."
    )


@eg037.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    cfr_status = is_cfr(session["ds_access_token"], session["ds_account_id"], session["ds_base_path"])
    if cfr_status == "enabled":
        if DS_CONFIG["quickstart"] == "true":
            return redirect(url_for("eg041.get_view"))
        else:
            return render_template("cfr_error.html", title="Error")

    return render_template(
        "eSignature/eg037_sms_delivery.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg037_sms_delivery.py",
        source_url=DS_CONFIG["github_example_url"] + "eg037_sms_delivery.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"]
    )

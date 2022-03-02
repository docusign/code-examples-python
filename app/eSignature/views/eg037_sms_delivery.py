""" Example 037: SMS Delivery """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg037_sms_delivery import Eg037SMSDeliveryController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg037"  # reference (and url) for this example
eg037 = Blueprint("eg037", __name__)


@eg037.route("/eg037", methods=["POST"])
@authenticate(eg=eg)
def sign_by_email():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

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
        title="Envelope sent",
        h1="Envelope sent",
        message=f"The envelope has been created and sent!<br/>Envelope ID {results['envelope_id']}."
    )


@eg037.route("/eg037", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg037_sms_delivery.html",
        title="SMS Delivery",
        source_file= "eg037_sms_delivery.py",
        source_url=DS_CONFIG["github_example_url"] + "eg037_sms_delivery.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

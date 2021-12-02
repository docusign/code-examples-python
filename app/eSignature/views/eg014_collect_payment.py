""" Example 014: Remote signer, cc; envelope has an order form """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, Blueprint

from ..examples.eg014_collect_payment import Eg014CollectPaymentController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg014"  # reference (and url) for this example
eg014 = Blueprint("eg014", __name__)


@eg014.route("/eg014", methods=["POST"])
@authenticate(eg=eg)
def collect_payment():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    # 1. Get required arguments
    args = Eg014CollectPaymentController.get_args()
    try:
        # 2. Call the worker method
        results = Eg014CollectPaymentController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render success response
    return render_template(
        "example_done.html",
        title="Envelope sent",
        h1="Envelope sent",
        message=f"""The envelope has been created and sent!<br/> Envelope ID {results["envelope_id"]}."""
    )


@eg014.route("/eg014", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    gateway = DS_CONFIG["gateway_account_id"]
    gateway_ok = gateway and len(gateway) > 25

    return render_template(
        "eg014_collect_payment.html",
        title="Order form with payment",
        source_file=path.basename(path.dirname(__file__)) + "/eg014_collect_payment.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg014_collect_payment.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"],
        gateway_ok=gateway_ok
    )

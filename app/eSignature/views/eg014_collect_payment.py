""" Example 014: Remote signer, cc; envelope has an order form """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ..examples.eg014_collect_payment import Eg014CollectPaymentController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 14
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg014 = Blueprint(eg, __name__)


@eg014.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def collect_payment():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

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
        title=example["ExampleName"],
        message=f"""The envelope has been created and sent!<br/> Envelope ID {results["envelope_id"]}."""
    )


@eg014.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    gateway = DS_CONFIG["gateway_account_id"]
    gateway_ok = gateway and len(gateway) > 25

    if "is_cfr" in session and session["is_cfr"] == "enabled":
        return render_template("cfr_error.html", title="Error")

    return render_template(
        "eSignature/eg014_collect_payment.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg014_collect_payment.py",
        source_url=DS_CONFIG["github_example_url"] + "eg014_collect_payment.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"],
        gateway_ok=gateway_ok
    )

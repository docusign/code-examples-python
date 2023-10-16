"""Example 044: Focused view"""

from docusign_esign.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ..examples.eg044_focused_view import Eg044FocusedViewController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 44
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg044 = Blueprint(eg, __name__)


@eg044.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def embedded_signing():
    """
    1. Get required arguments
    2. Call the worker method
    3. Redirect the user to the embedded signing
    """
    try:
        # 1. Get required arguments
        args = Eg044FocusedViewController.get_args()
        # 2. Call the worker method
        results = Eg044FocusedViewController.worker(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg044_embed.html",
        title=example["ExampleName"],
        url=results["redirect_url"],
        integration_key=DS_CONFIG["ds_client_id"]
    )


@eg044.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg044_focused_view.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg044_focused_view.py",
        source_url=DS_CONFIG["github_example_url"] + "eg044_focused_view.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

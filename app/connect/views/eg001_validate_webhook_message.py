"""Example 001: Validate webhook message using HMAC. """

from docusign_monitor.client.api_exception import ApiException
from flask import Blueprint, render_template, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg001_validate_webhook_message import Eg001ValidateWebhookMessageController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 1
api = API_TYPE["CONNECT"]
eg = f"cneg00{example_number}"  # Reference (and URL) for this example
cneg001 = Blueprint(eg, __name__)

@cneg001.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def get_monitoring_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)
    
    # 1. Get required arguments
    args = Eg001ValidateWebhookMessageController.get_args()
    try:
        # 2. Call the worker method to compute hash
        results = Eg001ValidateWebhookMessageController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"].format(results)
    )

@cneg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "connect/eg001_validate_webhook_message.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg001_validate_webhook_message.py",
        source_url=DS_CONFIG["connect_github_url"] + "eg001_validate_webhook_message.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


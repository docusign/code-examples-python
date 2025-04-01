"""Example 001: Set connected fields"""

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint, session

from ..examples.eg001_set_connected_fields import Eg001SetConnectedFieldsController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 1
api = API_TYPE["CONNECTED_FIELDS"]
eg = f"feg00{example_number}"  # reference (and url) for this example
feg001 = Blueprint(eg, __name__)


@feg001.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def set_connected_fields():
    """
    1. Get required arguments
    2. Call the worker method
    """
    try:
        # 1. Get required arguments
        args = Eg001SetConnectedFieldsController.get_args()
        # 2. Call the worker method
        selected_app = next((app for app in session["apps"] if app["appId"] == args["selected_app_id"]), None)
        results = Eg001SetConnectedFieldsController.send_envelope(args, selected_app)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]
    
    example = get_example_by_number(session["manifest"], example_number, api)
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"].format(results['envelope_id'])
    )


@feg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = {
        "account_id": session["ds_account_id"],
        "base_path": "https://api-d.docusign.com",
        "access_token": session["ds_access_token"],
    }
    apps = Eg001SetConnectedFieldsController.get_tab_groups(args)

    if not apps or len(apps) == 0:
        additional_page_data = next(
            (p for p in example["AdditionalPage"] if p["Name"] == "no_verification_app"), 
            None
        )
        
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=additional_page_data["ResultsPageText"]
        )

    session["apps"] = apps
    return render_template(
        "connected_fields/eg001_set_connected_fields.html",
        title=example["ExampleName"],
        example=example,
        apps=apps,
        source_file="eg001_set_connected_fields.py",
        source_url=DS_CONFIG["github_example_url"] + "eg001_set_connected_fields.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

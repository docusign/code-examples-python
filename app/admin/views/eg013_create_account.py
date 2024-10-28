"""Example 013: How to create an account. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg013_create_account import Eg013CreateAccountController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 13
api = API_TYPE["ADMIN"]
eg = f"aeg0{example_number}"  # Reference (and URL) for this example
aeg013 = Blueprint(eg, __name__)


@aeg013.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_account():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)
    
    # 1. Get required arguments
    args = Eg013CreateAccountController.get_args()
    try:
        # 2. Call the worker method to create an account
        results = Eg013CreateAccountController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"],
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@aeg013.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = Eg013CreateAccountController.get_args()

    try:
        plan_items = Eg013CreateAccountController.get_organization_plan_items(args)
        session["subscription_id"] = plan_items[0].subscription_id
        session["plan_id"] = plan_items[0].plan_id

    except ApiException as err:
        process_error(err)

    return render_template(
        "admin/eg013_create_account.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg013_create_account.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg013_create_account.py",
        documentation=DS_CONFIG["documentation"] + eg
    )


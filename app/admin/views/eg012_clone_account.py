"""Example 012: How to clone an account. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg012_clone_account import Eg012CloneAccountController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 12
api = API_TYPE["ADMIN"]
eg = f"aeg0{example_number}"  # Reference (and URL) for this example
aeg012 = Blueprint(eg, __name__)


@aeg012.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def audit_users():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)
    
    # 1. Get required arguments
    args = Eg012CloneAccountController.get_args()
    try:
        # 2. Call the worker method to clone the account
        results = Eg012CloneAccountController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"],
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@aeg012.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = Eg012CloneAccountController.get_args()

    try:
        accounts = Eg012CloneAccountController.get_accounts(args)
    except ApiException as err:
        process_error(err)

    return render_template(
        "admin/eg012_clone_account.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg012_clone_account.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg012_clone_account.py",
        documentation=DS_CONFIG["documentation"] + eg,
        accounts=accounts.asset_group_accounts
    )


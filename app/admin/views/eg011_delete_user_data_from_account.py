"""Example 011: Delete user data from an account as an account admin. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg011_delete_user_data_from_account import Eg011DeleteUserDataFromAccountController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 11
api = API_TYPE["ADMIN"]
eg = f"aeg0{example_number}"  # Reference (and URL) for this example
aeg011 = Blueprint(eg, __name__)


@aeg011.route(f"/{eg}", methods=["POST"])
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
    args = Eg011DeleteUserDataFromAccountController.get_args()
    try:
        # 2. Call the worker method to delete user data by user ID
        results = Eg011DeleteUserDataFromAccountController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"],
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@aeg011.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "admin/eg011_delete_user_data_from_account.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg011_delete_user_data_from_account.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg011_delete_user_data_from_account.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


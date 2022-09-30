"""Example 007: Get user profile data by user ID. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg007_get_user_profile_by_user_id import Eg007GetUserProfileByUserIdController
from ...ds_config import DS_CONFIG

example_number = 7
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg007 = Blueprint(eg, __name__)

@eg007.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def audit_users():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)
    
    # 1. Get required arguments
    args = Eg007GetUserProfileByUserIdController.get_args()
    try:
        # 2. Call the worker method to get user profile data by user ID
        results = Eg007GetUserProfileByUserIdController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from MultiProductUserManagement:getUserDSProfile method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg007.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    return render_template(
        f"{eg}_get_user_profile_by_user_id.html",
        title=example["ExampleName"],
        example=example,
        source_file=f"{eg}_get_user_profile_by_user_id.py",
        source_url=DS_CONFIG["admin_github_url"] + f"{eg}_get_user_profile_by_user_id.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


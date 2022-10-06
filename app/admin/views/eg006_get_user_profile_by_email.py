"""Example 006: Get user profile data by email. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg006_get_user_profile_by_email import Eg006GetUserProfileByEmailController
from ...ds_config import DS_CONFIG

example_number = 6
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg006 = Blueprint(eg, __name__)

@eg006.route(f"/{eg}", methods=["POST"])
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
    args = Eg006GetUserProfileByEmailController.get_args()
    try:
        # 2. Call the worker method to get user profile data by email
        results = Eg006GetUserProfileByEmailController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from MultiProductUserManagement:getUserDSProfilesByEmail method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg006.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    return render_template(
        f"{eg}_get_user_profile_by_email.html",
        title=example["ExampleName"],
        example=example,
        source_file=f"{eg}_get_user_profile_by_email.py",
        source_url=DS_CONFIG["admin_github_url"] + f"{eg}_get_user_profile_by_email.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


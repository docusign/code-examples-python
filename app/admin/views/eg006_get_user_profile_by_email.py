"""Example 006: Get user profile data by email. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg006_get_user_profile_by_email import Eg006GetUserProfileByEmailController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 6
api = API_TYPE["ADMIN"]
eg = f"aeg00{example_number}"  # Reference (and URL) for this example
aeg006 = Blueprint(eg, __name__)

@aeg006.route(f"/{eg}", methods=["POST"])
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

@aeg006.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        f"admin/eg006_get_user_profile_by_email.html",
        title=example["ExampleName"],
        example=example,
        source_file=f"eg006_get_user_profile_by_email.py",
        source_url=DS_CONFIG["admin_github_url"] + f"eg006_get_user_profile_by_email.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


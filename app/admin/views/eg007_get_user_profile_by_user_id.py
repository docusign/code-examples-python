"""Example 007: Get user profile data by user ID. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template

from app.docusign import authenticate
from app.error_handlers import process_error
from ..examples.eg007_get_user_profile_by_user_id import Eg007GetUserProfileByUserIdController
from ...ds_config import DS_CONFIG

eg = "eg007"  # Reference (and URL) for this example
eg007 = Blueprint(eg, __name__)

@eg007.route(f"/{eg}", methods=["POST"])
@authenticate(eg=eg)
def audit_users():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    
    # 1. Get required arguments
    args = Eg007GetUserProfileByUserIdController.get_args()
    try:
        # 2. Call the worker method to get user profile data by user ID
        results = Eg007GetUserProfileByUserIdController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title="Retrieve the user's DocuSign profile using a User ID",
        h1="Retrieve the user's DocuSign profile using a User ID",
        message="Results from MultiProductUserManagement:getUserDSProfile method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg007.route(f"/{eg}", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""

    return render_template(
        f"{eg}_get_user_profile_by_user_id.html",
        title="Get user profile data by email",
        source_file=f"{eg}_get_user_profile_by_user_id.py",
        source_url=DS_CONFIG["admin_github_url"] + f"{eg}_get_user_profile_by_user_id.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


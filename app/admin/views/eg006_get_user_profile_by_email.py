"""Example 006: Get user profile data by email. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template

from app.docusign import authenticate
from app.error_handlers import process_error
from ..examples.eg006_get_user_profile_by_email import Eg006GetUserProfileByEmailController
from ...ds_config import DS_CONFIG

eg = "eg006"  # Reference (and URL) for this example
eg006 = Blueprint(eg, __name__)

@eg006.route(f"/{eg}", methods=["POST"])
@authenticate(eg=eg)
def audit_users():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    
    # 1. Get required arguments
    args = Eg006GetUserProfileByEmailController.get_args()
    try:
        # 2. Call the worker method to get user profile data by email
        results = Eg006GetUserProfileByEmailController.worker(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title="Retrieve the user's DocuSign profile using an email address",
        h1="Retrieve the user's DocuSign profile using an email address",
        message="Results from MultiProductUserManagement:getUserDSProfilesByEmail method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg006.route(f"/{eg}", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""

    return render_template(
        f"{eg}_get_user_profile_by_email.html",
        title="Get user profile data by email",
        source_file=f"{eg}_get_user_profile_by_email.py",
        source_url=DS_CONFIG["admin_github_url"] + f"{eg}_get_user_profile_by_email.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


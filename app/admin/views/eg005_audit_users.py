"""Example 005: Audit users. """

import json
from os import path

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg005_audit_users import Eg005AuditUsersController
from ...ds_config import DS_CONFIG

example_number = 5
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg005 = Blueprint(eg, __name__)

@eg005.route(f"/{eg}", methods=["POST"])
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
    args = Eg005AuditUsersController.get_args()
    try:
        # 2. Call the worker method to get your monitor data
        results = Eg005AuditUsersController.worker(args)
        current_app.logger.info(f"""Auditing users""")
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from eSignUserManagement:getUserProfiles method:",
        json=json.dumps(json.dumps(results, default=str))
    )

@eg005.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    return render_template(
        "eg005_audit_users.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg005_audit_users.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg005_audit_users.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


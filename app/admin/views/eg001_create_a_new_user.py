"""Example 001: Create a new user"""

import json
from os import path

from flask import Blueprint, render_template, request, current_app, session
from docusign_admin.client.api_exception import ApiException

from app.error_handlers import process_error
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.ds_config import DS_CONFIG

from ..examples.eg001_create_a_new_user import Eg001CreateNewUserController

example_number = 1
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg001 = Blueprint(eg, __name__)

@eg001.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def get_user_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    controller = Eg001CreateNewUserController()

    # 1. Get required arguments
    args = Eg001CreateNewUserController.get_args(request)

    # 2. Call the worker method
    try:
        results = Eg001CreateNewUserController.worker(controller, args)
        current_app.logger.info(f"ID of the created user: {results.id}")
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from eSignUserManagement:createUser method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """
    Responds with the form for the example
    """
    example = get_example_by_number(session["manifest"], example_number)

    args = Eg001CreateNewUserController.get_args(request)
    
    try:
        profiles = Eg001CreateNewUserController.get_permission_profiles(args)
        groups = Eg001CreateNewUserController.get_groups(args)

    except ApiException as err:
        return process_error(err)

    # Render the response
    return render_template(
        "eg001_create_a_new_user.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg001_create_a_new_user.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg001_create_a_new_user.py",
        documentation=DS_CONFIG["documentation"] + eg,
        permission_profiles=profiles,
        groups=groups
    )

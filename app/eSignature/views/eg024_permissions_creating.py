"""Example 024: Creating a permission profile"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint, session

from ..examples.eg024_permissions_creating import Eg024PermissionsCreatingController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 24
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"
eg024 = Blueprint(eg, __name__)


@eg024.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def permissions_creating():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render a response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required args
    args = Eg024PermissionsCreatingController.get_args()
    try:
        # 2. Call the worker method to create a permission profile
        response = Eg024PermissionsCreatingController.worker(args)
        permission_profile_id = response.permission_profile_id
        app.logger.info(f"The permission profile has been created. Permission profile ID: {permission_profile_id}")

        # 3. Render the response
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"""The permission profile has been created!<br/> Permission profile ID: {permission_profile_id}."""
        )

    except ApiException as err:
        return process_error(err)

@eg024.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg024_permissions_creating.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg024_permissions_creating.py",
        source_url=DS_CONFIG["github_example_url"] + "eg024_permissions_creating.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        permission_profile_name="Sample Profile 134972-Alpha"
    )
"""Example 025: Set a permission profile for a group of users"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, request, Blueprint

from ..examples.eg025_permissions_set_user_group import Eg025PermissionsSetUserGroupController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 25
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"
eg025 = Blueprint(eg, __name__)

@eg025.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def permissions_set_user_group():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render a response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg025PermissionsSetUserGroupController.get_args()
    try:
        # 2. Call the worker method to set the permission profile
        response = Eg025PermissionsSetUserGroupController.worker(args)
        app.logger.info(f"The permission profile has been set.")
        permission_profile_id = response.groups[0].permission_profile_id
        group_id = response.groups[0].group_id

        # 3. Render the response
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"""The permission profile has been set!<br/>"""
                    f"""Permission profile ID: {permission_profile_id}<br/>"""
                    f"""Group id: {group_id}"""
        )

    except ApiException as err:
        return process_error(err)

@eg025.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = {
        "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
    }
    permission_profiles, groups = Eg025PermissionsSetUserGroupController.get_data(args)
    return render_template(
        "eSignature/eg025_permissions_set_user_group.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg025_permissions_set_user_group.py",
        source_url=DS_CONFIG["github_example_url"] + "eg025_permissions_set_user_group.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        permission_profiles=permission_profiles,
        groups=groups
    )
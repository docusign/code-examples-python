"""Example 026: Changing a single setting in a permission profile"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, Blueprint

from ..examples.eg026_permissions_change_single_setting import Eg026PermissionsChangeSingleSettingController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 26
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"
eg026 = Blueprint(eg, __name__)

@eg026.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def permissions_change_single_setting():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render a response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg026PermissionsChangeSingleSettingController.get_args()
    try:
        # 2. Call the worker method to change a setting in an existing permission profile
        response, changed_settings = Eg026PermissionsChangeSingleSettingController.worker(args)

        permission_profile_id = response.permission_profile_id

        app.logger.info(f"Permission profile setting has been changed. Permission profile ID: {permission_profile_id}")

        # 3. Render the response
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"""Setting of permission profile has been changed!<br/>"""
                    f"""Permission profile ID: {permission_profile_id}.<br> Changed settings:""",
            changed_settings=changed_settings
        )

    except ApiException as err:
        return process_error(err)

@eg026.route(f"/{eg}", methods=["GET"])
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
    permission_profiles = Eg026PermissionsChangeSingleSettingController.get_permissions_profiles(args)
    return render_template(
        "eSignature/eg026_permissions_change_single_setting.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg026_permissions_change_single_setting.py",
        source_url=DS_CONFIG["github_example_url"] + "eg026_permissions_change_single_setting.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        permission_profiles=permission_profiles
    )
"""Example 026: Changing a single setting in a permission profile"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, Blueprint

from .eg026_permissions_change_single_setting import Eg026PermissionsChangeSingleSettingController
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg026"
eg026 = Blueprint("eg026", __name__)

@eg026.route("/eg026", methods=["POST"])
@authenticate(eg=eg)
def permissions_change_single_setting():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render a response
    """

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
            title="Changing setting in a permission profile",
            h1="Changing setting in a permission profile",
            message=f"""Setting of permission profile has been changed!<br/>"""
                    f"""Permission profile ID: {permission_profile_id}.<br> Changed settings:""",
            changed_settings=changed_settings
        )

    except ApiException as err:
        return process_error(err)

@eg026.route("/eg026", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    args = {
        "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
    }
    permission_profiles = Eg026PermissionsChangeSingleSettingController.get_permissions_profiles(args)
    return render_template(
        "eg026_permissions_change_single_setting.html",
        title="Changing a setting in an existing permission profile",
        source_file=path.basename(path.dirname(__file__)) + "/eg026_permissions_change_single_setting.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg026_permissions_change_single_setting.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        permission_profiles=permission_profiles
    )
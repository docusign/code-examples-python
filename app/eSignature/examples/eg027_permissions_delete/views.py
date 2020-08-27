"""Example 027: Deleting a permission profile"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, request, Blueprint
from .controller import Eg027Controller
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg027"
eg027 = Blueprint("eg027", __name__)

@eg027.route("/eg027", methods=["POST"])
@authenticate(eg=eg)
def permissions_delete():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    args = Eg027Controller.get_args()
    try:
        # 2. Call the worker method to delete a permission profile
        Eg027Controller.worker(args)
        app.logger.info(f"The permission profile has been deleted.")

        # 3. Render success response
        return render_template(
            "example_done.html",
            title="Deleting a permission profile",
            h1="Deleting a permission profile",
            message=f"The permission profile has been deleted!<br/>"
        )

    except ApiException as err:
        return process_error(err)

@eg027.route("/eg027", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    args = {
        "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
    }
    permission_profiles = Eg027Controller.get_permissions_profiles(args)
    return render_template(
        "eg027_permissions_delete.html",
        title="Deleting a permission profile",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        permission_profiles=permission_profiles
    )
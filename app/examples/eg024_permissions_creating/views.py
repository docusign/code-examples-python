"""Example 024: Creating a permission profile"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint

from .controller import Eg024Controller
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg024"
eg024 = Blueprint("eg024", __name__)


@eg024.route("/eg024", methods=["POST"])
@authenticate(eg=eg)
def permissions_creating():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render a response
    """

    # 1. Get required args
    args = Eg024Controller.get_args()
    try:
        # 2. Call the worker method to create a permission profile
        response = Eg024Controller.worker(args)
        permission_profile_id = response.permission_profile_id
        app.logger.info(f"The permission profile has been created. Permission profile ID: {permission_profile_id}")

        # 3. Render the response
        return render_template(
            "example_done.html",
            title="Creating a permission profile",
            h1="Creating a permission profile",
            message=f"""The permission profile has been created!<br/> Permission profile ID: {permission_profile_id}."""
        )

    except ApiException as err:
        return process_error(err)

@eg024.route("/eg024", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg024_permissions_creating.html",
        title="Creating a permission profile",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        permission_profile_name="Sample Profile 134972-Alpha"
    )
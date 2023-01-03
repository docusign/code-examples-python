"""Example 027: Deleting a permission profile"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, request, Blueprint

from ..examples.eg027_permissions_delete import Eg027PermissionsDeleteController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 27
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"
eg027 = Blueprint(eg, __name__)

@eg027.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def permissions_delete():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    args = Eg027PermissionsDeleteController.get_args()
    try:
        # 2. Call the worker method to delete a permission profile
        Eg027PermissionsDeleteController.worker(args)
        app.logger.info(f"The permission profile has been deleted.")

        # 3. Render success response
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"The permission profile has been deleted!<br/>"
        )

    except ApiException as err:
        return process_error(err)

@eg027.route(f"/{eg}", methods=["GET"])
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
    permission_profiles = Eg027PermissionsDeleteController.get_permissions_profiles(args)
    return render_template(
        "eSignature/eg027_permissions_delete.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg027_permissions_delete.py",
        source_url=DS_CONFIG["github_example_url"] + "eg027_permissions_delete.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        permission_profiles=permission_profiles
    )
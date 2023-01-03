"""Example 009: Delete user product permission profiles using an email address. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg009_delete_user_product_permission_profile import Eg009DeleteUserProductPermissionProfileController
from ...ds_config import DS_CONFIG
from ..utils import check_user_exists_by_email
from ...consts import API_TYPE

example_number = 9
api = API_TYPE["ADMIN"]
eg = f"aeg00{example_number}"  # Reference (and URL) for this example
aeg009 = Blueprint(eg, __name__)

@aeg009.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_active_clm_esign_user():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    if "clm_email" in session and check_user_exists_by_email(session["clm_email"]):
        controller = Eg009DeleteUserProductPermissionProfileController()

        # 1. Get required arguments
        args = Eg009DeleteUserProductPermissionProfileController.get_args()
        try:
            # 2. Call the worker method
            results = Eg009DeleteUserProductPermissionProfileController.worker(controller, args)
        except ApiException as err:
            return process_error(err)

        template = render_template(
            "example_done.html",
            title=example["ExampleName"],
            message="Results from MultiProductUserManagement:removeUserProductPermission method:",
            json=json.dumps(json.dumps(results, default=str))
        )
    else:
        template = render_template(
            f"admin/eg009_delete_user_product_permission_profile.html",
            title=example["ExampleName"],
            example=example,
            source_file=f"eg009_delete_user_product_permission_profile.py",
            source_url=DS_CONFIG["admin_github_url"] + f"eg009_delete_user_product_permission_profile.py",
            documentation=DS_CONFIG["documentation"] + eg
        )

    return template

@aeg009.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    if "clm_email" in session and check_user_exists_by_email(session["clm_email"]):
        try:
            profiles = Eg009DeleteUserProductPermissionProfileController.get_permission_profiles_by_email()
            permission_profile_list = []
            clm_product_id = None
            clm_permission_profile_name = None
            esign_product_id = None
            esign_permission_profile_name = None
            for profile in profiles:
                permission_profiles = profile["permission_profiles"]
                for permission_profile in permission_profiles:
                    if profile["product_name"] == "CLM":
                        clm_permission_profile_name = permission_profile["permission_profile_name"]
                        clm_product_id = profile["product_id"]
                    else:
                        esign_permission_profile_name = permission_profile["permission_profile_name"]
                        esign_product_id = profile["product_id"]

            if clm_product_id is not None:
                permission_profile_list.append({"product_id": clm_product_id, "permission_name": f"CLM - {clm_permission_profile_name}"})

            if esign_product_id is not None:
                permission_profile_list.append({"product_id": esign_product_id, "permission_name": f"eSignature - {esign_permission_profile_name}"})

        except ApiException as err:
            return process_error(err)

        template = render_template(
            f"admin/eg009_delete_user_product_permission_profile.html",
            title=example["ExampleName"],
            example=example,
            email_ok="clm_email" in session,
            source_file=f"eg009_delete_user_product_permission_profile.py",
            source_url=DS_CONFIG["admin_github_url"] + f"eg009_delete_user_product_permission_profile.py",
            documentation=DS_CONFIG["documentation"] + eg,
            email=session["clm_email"],
            permission_profile_list=permission_profile_list
        )
    else:
        template = render_template(
            f"admin/eg009_delete_user_product_permission_profile.html",
            title=example["ExampleName"],
            example=example,
            source_file=f"eg009_delete_user_product_permission_profile.py",
            source_url=DS_CONFIG["admin_github_url"] + f"eg009_delete_user_product_permission_profile.py",
            documentation=DS_CONFIG["documentation"] + eg
        )

    return template

"""Example 008: Update user product permission profiles using an email address. """

import json

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, request, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg008_update_user_product_permission_profile import Eg008UpdateUserProductPermissionProfileController
from ...ds_config import DS_CONFIG
from ..utils import check_user_exists_by_email
from ...consts import API_TYPE

example_number = 8
api = API_TYPE["ADMIN"]
eg = f"aeg00{example_number}"  # Reference (and URL) for this example
aeg008 = Blueprint(eg, __name__)

@aeg008.route(f"/{eg}", methods=["POST"])
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
        controller = Eg008UpdateUserProductPermissionProfileController()

        # 1. Get required arguments
        args = Eg008UpdateUserProductPermissionProfileController.get_args()
        profiles = Eg008UpdateUserProductPermissionProfileController.get_permission_profiles()

        for profile in profiles:
            if profile["product_id"] == args["product_id"]:
                if profile["product_name"] == "CLM":
                    args["permission_profile_id"] = request.form.get("clm_permission_profile")
                else:
                    args["permission_profile_id"] = request.form.get("esign_permission_profile")

        try:
            # 2. Call the worker method
            results = Eg008UpdateUserProductPermissionProfileController.worker(controller, args)
        except ApiException as err:
            return process_error(err)

        template = render_template(
            "example_done.html",
            title=example["ExampleName"],
            message="Results from MultiProductUserManagement:addUserProductPermissionProfilesByEmail method:",
            json=json.dumps(json.dumps(results, default=str))
        )
    else:
        template = render_template(
            f"admin/eg008_create_active_clm_esign_user.html",
            title=example["ExampleName"],
            example=example,
            email_ok=False,
            source_file=f"eg008_create_active_clm_esign_user.py",
            source_url=DS_CONFIG["admin_github_url"] + f"eg008_create_active_clm_esign_user.py",
            documentation=DS_CONFIG["documentation"] + eg
        )

    return template

@aeg008.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    if "clm_email" in session and check_user_exists_by_email(session["clm_email"]):
        try:
            profiles = Eg008UpdateUserProductPermissionProfileController.get_permission_profiles()
            clm_permission_profiles_list = []
            esign_permission_profiles_list = []
            clm_product_id = ""
            esign_product_id = ""
            products_list = []
            for profile in profiles:
                permission_profiles = profile["permission_profiles"]
                for permission_profile in permission_profiles:
                    if profile["product_name"] == "CLM":
                        clm_permission_profiles_list.append(permission_profile)
                        clm_product_id = profile["product_id"]
                    else:
                        esign_permission_profiles_list.append(permission_profile)
                        esign_product_id = profile["product_id"]

            products_list.append({"product_id": clm_product_id, "product_name": "CLM"})
            products_list.append({"product_id": esign_product_id, "product_name": "eSignature"})

        except ApiException as err:
            return process_error(err)

        template = render_template(
            f"admin/eg008_update_user_product_permission_profile.html",
            title=example["ExampleName"],
            example=example,
            email_ok="clm_email" in session,
            source_file=f"eg008_update_user_product_permission_profile.py",
            source_url=DS_CONFIG["admin_github_url"] + f"eg008_update_user_product_permission_profile.py",
            documentation=DS_CONFIG["documentation"] + eg,
            product_list=products_list,
            email=session["clm_email"],
            clm_permission_profiles_list=clm_permission_profiles_list,
            esign_permission_profiles_list=esign_permission_profiles_list
        )
    else:
        template = render_template(
            f"admin/eg008_update_user_product_permission_profile.html",
            title=example["ExampleName"],
            example=example,
            email_ok=False,
            source_file=f"eg008_update_user_product_permission_profile.py",
            source_url=DS_CONFIG["admin_github_url"] + f"eg008_update_user_product_permission_profile.py",
            documentation=DS_CONFIG["documentation"] + eg
        )

    return template

"""Example 002: Create a new active user for CLM and eSignature. """

import json
from os import path

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg002_create_active_clm_esign_user import Eg002CreateActiveClmEsignUserController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 2
api = API_TYPE["ADMIN"]
eg = f"aeg00{example_number}"  # Reference (and URL) for this example
aeg002 = Blueprint(eg, __name__)

@aeg002.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_active_clm_esign_user():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    controller = Eg002CreateActiveClmEsignUserController()
    
    # 1. Get required arguments
    args = Eg002CreateActiveClmEsignUserController.get_args()
    try:
        # 2. Call the worker method to get your monitor data
        results = Eg002CreateActiveClmEsignUserController.worker(controller, args)
        current_app.logger.info(f"""Got your monitor data""")
    except ApiException as err:
        return process_error(err)

    session["clm_email"] = results["email"]  # Save for use by other examples which need an email of CLM user
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from MultiProductUserManagement:addOrUpdateUser method:",
        json=json.dumps(json.dumps(results, default=str))
    )

@aeg002.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    # Get the required arguments
    args = Eg002CreateActiveClmEsignUserController.get_args()

    try:
        profiles = Eg002CreateActiveClmEsignUserController.get_permission_profiles(args)
        clm_permission_profiles_list = []
        esign_permission_profiles_list = []
        for profile in profiles:
            permission_profiles = profile["permission_profiles"]
            for permission_profile in permission_profiles:
                if profile["product_name"] == "CLM":
                    clm_permission_profiles_list.append(permission_profile["permission_profile_name"])
                else: 
                    esign_permission_profiles_list.append(permission_profile["permission_profile_name"])

        ds_groups = Eg002CreateActiveClmEsignUserController.get_groups(args)
        ds_groups_dict = ds_groups.to_dict()
        ds_groups_list = ds_groups_dict["ds_groups"]
    
    except ApiException as err:
        return process_error(err)

    return render_template(
        "admin/eg002_create_active_clm_esign_user.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg002_create_active_clm_esign_user.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg002_create_active_clm_esign_user.py",
        documentation=DS_CONFIG["documentation"] + eg,
        clm_permission_profiles_list=clm_permission_profiles_list,
        esign_permission_profiles_list=esign_permission_profiles_list,
        ds_groups=ds_groups_list
    )

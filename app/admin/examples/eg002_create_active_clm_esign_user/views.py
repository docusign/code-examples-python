"""Example 002: Create a new active user for CLM and eSignature. """

import json
from os import path

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app

from app.docusign import authenticate
from app.error_handlers import process_error
from .controller import Eg002Controller
from ....ds_config import DS_CONFIG

eg = "eg002"  # Reference (and URL) for this example
eg002 = Blueprint(eg, __name__)

@eg002.route("/eg002", methods=["POST"])
@authenticate(eg=eg)
def create_active_clm_esign_user():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """

    controller = Eg002Controller()
    
    # 1. Get required arguments
    args = Eg002Controller.get_args()
    try:
        # 2. Call the worker method to get your monitor data
        results = Eg002Controller.worker(controller, args)
        current_app.logger.info(f"""Got your monitor data""")
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title="Create a new active user for CLM and eSignature",
        h1="Create active user for CLM and eSignature",
        message="Results from Users::addOrUpdateUser method:",
        json=json.dumps(json.dumps(results, default=str))
    )

@eg002.route("/eg002", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""

    # Get the required arguments
    args = Eg002Controller.get_args()

    try:
        profiles = Eg002Controller.get_permission_profiles(args)
        clm_permission_profiles_list = []
        esign_permission_profiles_list = []
        for profile in profiles:
            permission_profiles = profile["permission_profiles"]
            for permission_profile in permission_profiles:
                if profile["product_name"] == "CLM":
                    clm_permission_profiles_list.append(permission_profile["permission_profile_name"])
                else: 
                    esign_permission_profiles_list.append(permission_profile["permission_profile_name"])

        ds_groups = Eg002Controller.get_groups(args)
        ds_groups_dict = ds_groups.to_dict()
        ds_groups_list = ds_groups_dict["ds_groups"]
    
    except ApiException as err:
        return process_error(err)


    return render_template(
        "eg002_create_active_clm_esign_user.html",
        title="Create an active CLM + eSign user",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["admin_github_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        clm_permission_profiles_list=clm_permission_profiles_list,
        esign_permission_profiles_list=esign_permission_profiles_list,
        ds_groups=ds_groups_list
    )

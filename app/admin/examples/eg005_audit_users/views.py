"""Example 005: Audit users. """

import json
from os import path

from docusign_admin.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app

from app.docusign import authenticate
from app.error_handlers import process_error
from .controller import Eg005Controller
from ....ds_config import DS_CONFIG

eg = "eg005"  # Reference (and URL) for this example
eg005 = Blueprint(eg, __name__)

@eg005.route("/eg005", methods=["POST"])
@authenticate(eg=eg)
def audit_users():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    
    # 1. Get required arguments
    args = Eg005Controller.get_args()
    try:
        # 2. Call the worker method to get your monitor data
        results = Eg005Controller.worker(args)
        current_app.logger.info(f"""Auditing users""")
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title="Audit users",
        h1="Audit users",
        message="Results from eSignUserManagement:getUserProfiles method:",
        json=json.dumps(json.dumps(results, default=str))
    )

@eg005.route("/eg005", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""


    return render_template(
        "eg005_audit_users.html",
        title="Audit users",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["admin_github_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


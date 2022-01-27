"""Example 003: Creating a new clickwrap version"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg003_create_new_clickwrap_version import Eg003CrateNewClickwrapVersionController
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

eg = "eg003"  # Reference (and URL) for this example
eg003 = Blueprint("eg003", __name__)


@eg003.route("/eg003", methods=["POST"])
@authenticate(eg=eg)
def create_new_clickwrap_version():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg003CrateNewClickwrapVersionController.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap version
        results = Eg003CrateNewClickwrapVersionController.worker(args)
        results_dict = results.to_dict()
        current_app.logger.info(
            f"""Version {results_dict['version_number']} of clickwrap "{results_dict['clickwrap_name']}" has been created."""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Create a new clickwrap version",
        h1="Create a new clickwrap version",
        message=f"""Version {results_dict['version_number']} of clickwrap "{results_dict['clickwrap_name']}" has been created.""",
        json=json.dumps(json.dumps(results_dict, default=str))
    )


@eg003.route("/eg003", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg003_create_new_clickwrap_version.html",
        title="Creating a new clickwrap version",
        clickwrap_ok="clickwrap_id" in session,
        source_file= "eg003_create_new_clickwrap_version.py",
        source_url=DS_CONFIG["click_github_url"] + "eg003_create_new_clickwrap_version.py",
    )

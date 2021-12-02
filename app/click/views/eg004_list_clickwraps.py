"""Example 004: Getting a list of clickwraps"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg004_list_clickwraps import Eg004ListClickwrapsController
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

eg = "eg004"  # Reference (and URL) for this example
eg004 = Blueprint("eg004", __name__)


@eg004.route("/eg004", methods=["POST"])
@authenticate(eg=eg)
def clickwrap_list():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg004ListClickwrapsController.get_args()

    try:
        # 2. Call the worker method to get a list of clickwraps
        results = Eg004ListClickwrapsController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="List clickwraps results",
        h1="List clickwraps results",
        message="Results from the ClickWraps::getClickwraps method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg004.route("/eg004", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""
    return render_template(
        "eg004_list_clickwraps.html",
        title="Getting a list of clickwraps",
        source_file=path.basename(path.dirname(__file__)) + "/eg004_list_clickwraps.py",
        source_url=DS_CONFIG["click_github_url"] + path.basename(
            path.dirname(__file__)) + "/eg004_list_clickwraps.py",
    )

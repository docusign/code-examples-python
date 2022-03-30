"""Example 005: Getting clickwrap responses"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg005_clickwrap_responses import Eg005ClickwrapResponsesController
from ..examples.eg004_list_clickwraps import Eg004ListClickwrapsController
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

eg = "eg005"  # Reference (and URL) for this example
eg005 = Blueprint("eg005", __name__)


@eg005.route("/eg005", methods=["POST"])
@authenticate(eg=eg)
def clickwrap_responses():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg005ClickwrapResponsesController.get_args()

    try:
        # 2. Call the worker method to get clickwrap responses
        results = Eg005ClickwrapResponsesController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Get clickwrap responses",
        h1="Get clickwrap responses",
        message="Results from the ClickWraps::getClickwrapAgreements method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg005.route("/eg005", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""
    args = Eg004ListClickwrapsController.get_args()
    return render_template(
        "eg005_clickwrap_responses.html",
        title="Getting clickwrap responses",
        clickwraps_data=Eg004ListClickwrapsController.worker(args),
        source_file= "eg005_clickwrap_responses.py",
        source_url=DS_CONFIG["click_github_url"] + "eg005_clickwrap_responses.py",
    )

"""Example 005: Getting clickwrap responses"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg005_clickwrap_responses import Eg005ClickwrapResponsesController
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
        title="Getting clickwrap responses",
        h1="Getting clickwrap responses",
        message="Results from the ClickWraps::getClickwrapAgreements method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg005.route("/eg005", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""
    return render_template(
        "eg005_clickwrap_responses.html",
        title="Getting clickwrap responses",
        clickwrap_ok="clickwrap_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/eg005_clickwrap_responses.py",
        source_url=DS_CONFIG["click_github_url"] + path.basename(
            path.dirname(__file__)) + "/eg005_clickwrap_responses.py",
    )

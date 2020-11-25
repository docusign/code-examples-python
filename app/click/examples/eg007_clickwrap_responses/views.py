"""Example 007: Getting clickwrap responses"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from .controller import Eg007Controller
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

eg = "eg007"  # reference (and url) for this example
eg007 = Blueprint("eg007", __name__)


@eg007.route("/eg007", methods=["POST"])
@authenticate(eg=eg)
def clickwrap_responses():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg007Controller.get_args()

    try:
        # 2. Call the worker method to get clickwrap responses
        results = Eg007Controller.worker(args)
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


@eg007.route("/eg007", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg007_clickwrap_responses.html",
        title="Getting clickwrap responses",
        clickwrap_ok="clickwrap_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(
            path.dirname(__file__)) + "/controller.py",
    )

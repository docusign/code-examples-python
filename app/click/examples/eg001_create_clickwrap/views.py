"""Example 001: Creating a clickwrap"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from .controller import Eg001Controller
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

eg = "eg001"  # Reference (and URL) for this example
eg001 = Blueprint("eg001", __name__)


@eg001.route("/eg001", methods=["POST"])
@authenticate(eg=eg)
def create_clickwrap():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg001Controller.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap
        results = Eg001Controller.worker(args)
        clickwrap_id = results.clickwrap_id
        clickwrap_name = args['clickwrap_name']
        current_app.logger.info(
            f"""The clickwrap "{clickwrap_name}" has been created!"""
        )
    except ApiException as err:
        return process_error(err)

    # Save for use by other examples which need a clickwrap parameter.
    session["clickwrap_id"] = clickwrap_id
    session["clickwrap_name"] = clickwrap_name
    session["clickwrap_is_active"] = False

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Creating a new clickwrap",
        h1="Creating a new clickwrap",
        message=f"""The clickwrap "{args['clickwrap_name']}" has been created!""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg001.route("/eg001", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg001_create_clickwrap.html",
        title="Creating a new clickwrap",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(
            path.dirname(__file__)) + "/controller.py",
    )

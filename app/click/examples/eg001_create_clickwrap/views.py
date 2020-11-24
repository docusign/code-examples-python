"""Example 001: Creating a clickwrap"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint

from .controller import Eg001Controller
from app.docusign import authenticate
from app.error_handlers import process_error

eg = "eg001"  # reference (and url) for this example
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
        current_app.logger.info(
            f"""The clickwrap "{args['clickwrap_name']}" has been created! clickwrap ID: {clickwrap_id}"""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Creating a new clickwrap",
        h1="Creating a new clickwrap",
        message=f"""The clickwrap "{args['clickwrap_name']}" has been created!<br/>
                        Clickwrap ID: {clickwrap_id}.""",
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
    )

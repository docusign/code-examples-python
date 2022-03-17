"""Example 002: Activating a clickwrap"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg002_activate_clickwrap import Eg002ActivateClickwrapController
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

eg = "eg002"  # Reference (and URL) for this example
eg002 = Blueprint("eg002", __name__)


@eg002.route("/eg002", methods=["POST"])
@authenticate(eg=eg)
def activate_clickwrap():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg002ActivateClickwrapController.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap
        results = Eg002ActivateClickwrapController.worker(args)
        current_app.logger.info(
            f"""The clickwrap "{args['clickwrap_name']}" has been activated."""
        )
    except ApiException as err:
        return process_error(err)

    # Save for use by other examples which need an clickwrap params.
    session["clickwrap_is_active"] = True

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Activate a clickwrap",
        h1="Activate a clickwrap",
        message=f"""The clickwrap "{args['clickwrap_name']}" has been activated!""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg002.route("/eg002", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    args = Eg002ActivateClickwrapController.get_args()
    return render_template(
        "eg002_activate_clickwrap.html",
        title="Activating a clickwrap",
        clickwrapData=Eg002ActivateClickwrapController.get_inactive_clickwraps(),
        source_file= "eg002_activate_clickwrap.py",
        source_url=DS_CONFIG["click_github_url"] + "eg002_activate_clickwrap.py",
    )

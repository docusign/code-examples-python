"""Example 002: Activating a clickwrap"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg002_activate_clickwrap import Eg002ActivateClickwrapController
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 2
api = API_TYPE["CLICK"]
eg = f"ceg00{example_number}"  # Reference (and URL) for this example
ceg002 = Blueprint(eg, __name__)


@ceg002.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def activate_clickwrap():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg002ActivateClickwrapController.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap
        results = Eg002ActivateClickwrapController.worker(args)
        current_app.logger.info(
            f"""The clickwrap has been activated."""
        )
    except ApiException as err:
        return process_error(err)

    # Save for use by other examples which need an clickwrap params.
    session["clickwrap_is_active"] = True

    # 3. Render the response
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=f"""The clickwrap has been activated!""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@ceg002.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = Eg002ActivateClickwrapController.get_args()
    return render_template(
        "click/eg002_activate_clickwrap.html",
        title=example["ExampleName"],
        example=example,
        clickwraps_data=Eg002ActivateClickwrapController.get_inactive_clickwraps(args),
        source_file= "eg002_activate_clickwrap.py",
        source_url=DS_CONFIG["click_github_url"] + "eg002_activate_clickwrap.py",
    )

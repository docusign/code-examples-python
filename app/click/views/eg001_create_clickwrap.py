"""Example 001: Creating a clickwrap"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg001_create_clickwrap import Eg001CreateClickwrapController
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 1
api = API_TYPE["CLICK"]
eg = f"ceg00{example_number}"  # Reference (and URL) for this example
ceg001 = Blueprint(eg, __name__)


@ceg001.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_clickwrap():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg001CreateClickwrapController.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap
        results = Eg001CreateClickwrapController.worker(args)
        clickwrap_id = results.clickwrap_id
        clickwrap_name = args['clickwrap_name']
        current_app.logger.info(
            f"""The clickwrap "{clickwrap_name}" has been created."""
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
        title=example["ExampleName"],
        message=f"""The clickwrap "{args['clickwrap_name']}" has been created!""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@ceg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "click/eg001_create_clickwrap.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg001_create_clickwrap.py",
        source_url=DS_CONFIG["click_github_url"] + "eg001_create_clickwrap.py",
    )

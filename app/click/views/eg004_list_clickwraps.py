"""Example 004: Getting a list of clickwraps"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg004_list_clickwraps import Eg004ListClickwrapsController
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 4
api = API_TYPE["CLICK"]
eg = f"ceg00{example_number}"  # Reference (and URL) for this example
ceg004 = Blueprint(eg, __name__)


@ceg004.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def clickwrap_list():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

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
        title=example["ExampleName"],
        message="Results from the ClickWraps::getClickwraps method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@ceg004.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "click/eg004_list_clickwraps.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg004_list_clickwraps.py",
        source_url=DS_CONFIG["click_github_url"] + "eg004_list_clickwraps.py",
    )

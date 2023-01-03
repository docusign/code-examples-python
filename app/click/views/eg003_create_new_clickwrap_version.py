"""Example 003: Creating a new clickwrap version"""

from os import path
import json

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg003_create_new_clickwrap_version import Eg003CrateNewClickwrapVersionController
from ..examples.eg004_list_clickwraps import Eg004ListClickwrapsController
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 3
api = API_TYPE["CLICK"]
eg = f"ceg00{example_number}"  # Reference (and URL) for this example
ceg003 = Blueprint(eg, __name__)


@ceg003.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_new_clickwrap_version():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg003CrateNewClickwrapVersionController.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap version
        results = Eg003CrateNewClickwrapVersionController.worker(args)
        results_dict = results.to_dict()
        current_app.logger.info(
            f"""Version {results_dict['version_number']} of clickwrap "{results_dict['clickwrap_name']}" has been created."""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=f"""Version {results_dict['version_number']} of clickwrap "{results_dict['clickwrap_name']}" has been created.""",
        json=json.dumps(json.dumps(results_dict, default=str))
    )


@ceg003.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = Eg004ListClickwrapsController.get_args()
    return render_template(
        "click/eg003_create_new_clickwrap_version.html",
        title=example["ExampleName"],
        example=example,
        clickwraps_data=Eg004ListClickwrapsController.worker(args),
        source_file= "eg003_create_new_clickwrap_version.py",
        source_url=DS_CONFIG["click_github_url"] + "eg003_create_new_clickwrap_version.py",
    )

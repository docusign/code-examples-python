import json
from os import path

from docusign_rooms.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from ...ds_config import DS_CONFIG
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ..examples.eg007_create_form_group import Eg007CreateFormGroupController

example_number = 7
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg007 = Blueprint(eg, __name__)


@eg007.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def create_form_group():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg007CreateFormGroupController.get_args()

    try:
        # 2. Call the worker method to create a new form group
        results = Eg007CreateFormGroupController.worker(args)
        form_id = results.form_group_id
        current_app.logger.info(
            f"""Form Group "{args['form_group_name']}" has been created! 
            Form Group ID: {form_id}"""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Creating a form group",
        h1="Creating a form group",
        message=f"""The Form Group "{args['form_group_name']}" has been created!<br/> 
                            Room ID: {form_id}.""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg007.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    return render_template(
        "eg007_create_form_group.html",
        title="Creating a form group",
        source_file= "eg007_create_form_group.py"
    )

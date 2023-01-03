import json
from os import path

from docusign_rooms.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from ...ds_config import DS_CONFIG
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ..examples.eg007_create_form_group import Eg007CreateFormGroupController
from ...consts import API_TYPE

example_number = 7
api = API_TYPE["ROOMS"]
eg = f"reg00{example_number}"  # Reference (and URL) for this example
reg007 = Blueprint(eg, __name__)


@reg007.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_form_group():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

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
        title=example["ExampleName"],
        message=f"""The Form Group "{args['form_group_name']}" has been created!<br/> 
                            Room ID: {form_id}.""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@reg007.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "rooms/eg007_create_form_group.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg007_create_form_group.py"
    )

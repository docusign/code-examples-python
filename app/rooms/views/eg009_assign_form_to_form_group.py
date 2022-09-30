import json
from os import path

from docusign_rooms.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from ...ds_config import DS_CONFIG
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ..examples.eg009_assign_form_to_form_group import Eg009AssignFormToFormGroupController

example_number = 9
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg009 = Blueprint(eg, __name__)


@eg009.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def assign_form_to_form_group():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg009AssignFormToFormGroupController.get_args()

    try:
        # 2. Call the worker method to create a new form group
        results = Eg009AssignFormToFormGroupController.worker(args)
        current_app.logger.info(
            f"""Form "{args['form_id']}" has been assigned to 
            Form Group "{args['form_group_id']}"!"""
        )
        results = results.to_dict()
    except ApiException as err:
        return process_error(err)
    except ValueError as err:
        msg = ("Response is empty and could not be cast to"
               " FormGroupFormToAssign. Please contact DocuSign support.")
        current_app.logger.info(msg)
        results = {"error": msg}

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Assigning form a form group",
        h1="Creating a form group",
        message=f"""Form "{args['form_id']}" has been assigned to 
        Form Group "{args['form_group_id']}"!""",
    )


@eg009.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get form groups
    3. Get forms
    4. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg009AssignFormToFormGroupController.get_args()

    # 2. Get form groups
    form_groups = Eg009AssignFormToFormGroupController.get_form_groups(args)

    # 3. Get forms
    forms = Eg009AssignFormToFormGroupController.get_forms(args)

    # 4. Render the response
    return render_template(
        "eg009_assign_form_to_form_group.html",
        forms=forms,
        form_groups=form_groups,
        source_file=path.basename(path.dirname(__file__)) + "\controller.py",
        source_url="https://github.com/docusign/code-examples-python/tree/master/app/" + path.relpath(path.dirname(__file__), start='app') + "/controller.py",
    )

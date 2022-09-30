from docusign_rooms.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from os import path

from ...ds_config import DS_CONFIG
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ..examples.eg008_grant_office_access_to_form_group import Eg008GrantOfficeAccessToFormGroupController

example_number = 8
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg008 = Blueprint(eg, __name__)


@eg008.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def assign_office_to_form_group():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    args = Eg008GrantOfficeAccessToFormGroupController.get_args()

    try:
        # 2. Call the worker method to assign office to form group
        Eg008GrantOfficeAccessToFormGroupController.worker(args)
        current_app.logger.info(
            f"""Office {args['office_id']} has been assigned to Form Group
            {args['form_group_id']}!"""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Assign office to a form group",
        h1="Assign office to a form group",
        message=f"""Office "{args['office_id']}" has been assigned to 
        Form Group "{args['form_group_id']}" """,
    )


@eg008.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get Form Groups
    3. Get Offices
    4. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg008GrantOfficeAccessToFormGroupController.get_args()

    # 2. Get Form Groups
    form_groups = Eg008GrantOfficeAccessToFormGroupController.get_form_groups(args)

    # 3. Get offices
    offices = Eg008GrantOfficeAccessToFormGroupController.get_offices(args)

    # 4. Render the response
    return render_template(
        "eg008_grant_office_access_to_form_group.html",
        offices=offices,
        form_groups=form_groups,
        source_file=path.basename(path.dirname(__file__)) + "\controller.py",
        source_url="https://github.com/docusign/code-examples-python/tree/master/app/" + path.relpath(path.dirname(__file__), start='app') + "/controller.py",
    )

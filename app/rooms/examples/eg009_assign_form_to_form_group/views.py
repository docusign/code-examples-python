import json

from docusign_rooms.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app

from app.docusign import authenticate
from app.error_handlers import process_error
from .controller import Eg009Controller

eg = "eg009"  # reference (and URL) for this example
eg009 = Blueprint(eg, __name__)


@eg009.route("/eg009", methods=["POST"])
@authenticate(eg=eg)
def assign_form_to_form_group():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """

    # 1. Get required arguments
    args = Eg009Controller.get_args()

    try:
        # 2. Call the worker method to create a new form group
        results = Eg009Controller.worker(args)
        current_app.logger.info(
            f"""Form "{args['form_id']}" has been assigned to 
            Form Group "{args['form_group_id']}"!"""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Assigning form a form group",
        h1="Creating a form group",
        message=f"""Form "{args['form_id']}" has been assigned to 
        Form Group "{args['form_group_id']}"!""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg009.route("/eg009", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get form groups
    3. Get forms
    4. Render the response
    """

    # 1. Get required arguments
    args = Eg009Controller.get_args()

    # 2. get form groups
    form_groups = Eg009Controller.get_form_groups(args)

    # 3. get forms
    forms = Eg009Controller.get_forms(args)

    # 4. Render the response
    return render_template(
        "eg009_assign_form_to_form_group.html",
        forms=forms,
        form_groups=form_groups
    )

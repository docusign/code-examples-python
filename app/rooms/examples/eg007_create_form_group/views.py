import json
from os import path

from docusign_rooms.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app

from app.docusign import authenticate
from app.error_handlers import process_error
from .controller import Eg007Controller

eg = "eg007"  # Reference (and URL) for this example
eg007 = Blueprint(eg, __name__)


@eg007.route("/eg007", methods=["POST"])
@authenticate(eg=eg)
def create_form_group():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """

    # 1. Get required arguments
    args = Eg007Controller.get_args()

    try:
        # 2. Call the worker method to create a new form group
        results = Eg007Controller.worker(args)
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


@eg007.route("/eg007", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg007_create_form_group.html",
        title="Creating a form group",
        source_file=path.basename(path.dirname(__file__)) + "\controller.py",
        source_url="https://github.com/docusign/code-examples-python/tree/master/app/" + path.relpath(path.dirname(__file__), start='app') + "/controller.py",
    )

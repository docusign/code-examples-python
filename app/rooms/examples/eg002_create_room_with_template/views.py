"""Example 002: Creating a room with template"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint

from .controller import Eg002Controller
from app.docusign import authenticate
from app.error_handlers import process_error

eg = "eg002"  # reference (and url) for this example
eg002 = Blueprint("eg002", __name__)


@eg002.route("/eg002", methods=["POST"])
@authenticate(eg=eg)
def create_room_with_template():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg002Controller.get_args()

    try:
        # 2. Call the worker method to create a new room
        results = Eg002Controller.worker(args)
        room_id = results.room_id
        current_app.logger.info(
            f"""Room "{args['room_name']}" has been created! Room ID: {room_id}"""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Creating a room with a template",
        h1="Creating a room with a template",
        message=f"""The room "{args['room_name']}" has been created!<br/>
                        Room ID: {room_id}.""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg002.route("/eg002", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get room templates
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg002Controller.get_args()

    try:
        # 2. Get room templates
        templates = Eg002Controller.get_templates(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "eg002_create_room_with_template.html",
        title="Creating a room with a template",
        source_file=path.basename(path.dirname(__file__)) + "\controller.py",
        source_url="https://github.com/docusign/code-examples-python/tree/master/app/" + path.relpath(path.dirname(__file__), start='app') + "/controller.py",
        templates=templates
    )

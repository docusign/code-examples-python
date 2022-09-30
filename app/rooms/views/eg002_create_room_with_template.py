"""Example 002: Creating a room with template"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ...ds_config import DS_CONFIG
from ..examples.eg002_create_room_with_template import Eg002CreateRoomWithTemplateController
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error

example_number = 2
eg = f"eg00{example_number}"  # reference (and url) for this example
eg002 = Blueprint(eg, __name__)


@eg002.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def create_room_with_template():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg002CreateRoomWithTemplateController.get_args()

    try:
        # 2. Call the worker method to create a new room
        results = Eg002CreateRoomWithTemplateController.worker(args)
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


@eg002.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get room templates
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg002CreateRoomWithTemplateController.get_args()

    try:
        # 2. Get room templates
        templates = Eg002CreateRoomWithTemplateController.get_templates(args)
    except ApiException as err:
        return process_error(err)

    return render_template(
        "eg002_create_room_with_template.html",
        title="Creating a room with a template",
        source_file= "eg002_create_room_with_template.py",
        templates=templates
    )

"""Example 001: Creating a room with data"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ...ds_config import DS_CONFIG
from ..examples.eg001_create_room_with_data import Eg001CreateRoomWithDateController
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error

example_number = 1
eg = "eg001"  # reference (and url) for this example
eg001Rooms = Blueprint("eg001", __name__)


@eg001Rooms.route("/eg001", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    return render_template(
        "eg001_create_room_with_data.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg001_create_room_with_data.py",
    )


@eg001Rooms.route("/eg001", methods=["POST"])
@authenticate(eg=eg)
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
def create_room_with_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg001CreateRoomWithDateController.get_args()

    try:
        # 2. Call the worker method to create a new room
        results = Eg001CreateRoomWithDateController.worker(args)
        room_id = results.room_id
        current_app.logger.info(
            f"""Room "{args['room_name']}" has been created! Room ID: {room_id}"""
        )
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=f"""The room "{args['room_name']}" has been created!<br/> 
                        Room ID: {room_id}.""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

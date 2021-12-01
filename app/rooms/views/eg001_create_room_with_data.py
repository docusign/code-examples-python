"""Example 001: Creating a room with data"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint

from .eg001_create_room_with_data import Eg001CreateRoomWithDateController
from app.docusign import authenticate
from app.error_handlers import process_error

eg = "eg001Rooms"  # reference (and url) for this example
eg001Rooms = Blueprint("eg001Rooms", __name__)


@eg001Rooms.route("/eg001Rooms", methods=["POST"])
@authenticate(eg=eg)
def create_room_with_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
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
        title="Creating a room with data",
        h1="Creating a room with data",
        message=f"""The room "{args['room_name']}" has been created!<br/> 
                        Room ID: {room_id}.""",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg001Rooms.route("/eg001Rooms", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg001_create_room_with_data.html",
        title="Creating a room with data",
        source_file=path.basename(path.dirname(__file__)) + "/eg001_create_room_with_data.py",
    )

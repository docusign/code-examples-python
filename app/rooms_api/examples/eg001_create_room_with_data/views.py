"""Example 001: Creating a room with data"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint

from .controller import Eg001Controller
from app.docusign import authenticate
from app.error_handlers import process_error

eg = "eg001"  # reference (and url) for this example
eg001 = Blueprint("eg001", __name__)


@eg001.route("/eg001", methods=["POST"])
@authenticate(eg=eg)
def create_room_with_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg001Controller.get_args()

    try:
        # 2. Call the worker method to create a new room
        response = Eg001Controller.worker(args)
        room_id = response.room_id
        current_app.logger.info(f"""Room "{args['room_name']}" has been created! Room ID: {room_id}""")

        # 3. Render the response
        return render_template(
            "example_done.html",
            title="Creating a room with data",
            h1="Creating a room with data",
            message=f"""The room "{args['room_name']}" has been created!<br/> Room ID: {room_id}.""",
        )
    except ApiException as err:
        return process_error(err)


@eg001.route("/eg001", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    return render_template(
        "eg001_create_room_with_data.html",
        title="Creating a room with data",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
    )

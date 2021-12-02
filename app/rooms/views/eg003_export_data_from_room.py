"""Example 003: Exporting data from a room"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, Blueprint

from ..examples.eg003_export_data_from_room import Eg003ExportDataFromRoomController
from app.docusign import authenticate
from app.error_handlers import process_error

eg = "eg003"  # reference (and URL) for this example
eg003 = Blueprint("eg003", __name__)


@eg003.route("/eg003", methods=["POST"])
@authenticate(eg=eg)
def get_field_data_from_room():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg003ExportDataFromRoomController.get_args()

    try:
        # 2. Call the worker method
        results = Eg003ExportDataFromRoomController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Show field data
    return render_template(
        "example_done.html",
        title="Field data associated with a room",
        h1="Field data associated with a room",
        message="Results from the Rooms::GetRoomFieldData method:",
        json=json.dumps(json.dumps(results.to_dict()))
    )


@eg003.route("/eg003", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get rooms
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg003ExportDataFromRoomController.get_args()

    try:
        # 2. Get rooms
        rooms = Eg003ExportDataFromRoomController.get_rooms(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "eg003_export_data_from_room.html",
        title="Exporting data from a room",
        source_file=path.basename(path.dirname(__file__)) + "/eg003_export_data_from_room.py",
        rooms=rooms,
    )

"""Example 003: Exporting data from a room"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ...ds_config import DS_CONFIG
from ..examples.eg003_export_data_from_room import Eg003ExportDataFromRoomController
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 3
api = API_TYPE["ROOMS"]
eg = f"reg00{example_number}"  # reference (and URL) for this example
reg003 = Blueprint(eg, __name__)


@reg003.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_field_data_from_room():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

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
        title=example["ExampleName"],
        message="Results from the Rooms::GetRoomFieldData method:",
        json=json.dumps(json.dumps(results.to_dict()))
    )


@reg003.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """
    1. Get required arguments
    2. Get rooms
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg003ExportDataFromRoomController.get_args()

    try:
        # 2. Get rooms
        rooms = Eg003ExportDataFromRoomController.get_rooms(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "rooms/eg003_export_data_from_room.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg003_export_data_from_room.py",
        rooms=rooms,
    )

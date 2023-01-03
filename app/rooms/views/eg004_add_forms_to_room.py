"""Example 004: Adding forms to a room"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ...ds_config import DS_CONFIG
from ..examples.eg004_add_forms_to_room import Eg004AddFormsToRoomController
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 4
api = API_TYPE["ROOMS"]
eg = f"reg00{example_number}"  # reference (and URL) for this example
reg004 = Blueprint(eg, __name__)


@reg004.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def add_form_to_room():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show room document
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg004AddFormsToRoomController.get_args()

    try:
        # 2. Call the worker method
        results = Eg004AddFormsToRoomController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Show filtered rooms
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from the Rooms::AddFormToRoom method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@reg004.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """
    1. Get required arguments
    2. Get rooms
    3. Get forms
    4. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg004AddFormsToRoomController.get_args()

    try:
        # 2. Get rooms
        rooms = Eg004AddFormsToRoomController.get_rooms(args)
        # 3. Get forms
        forms = Eg004AddFormsToRoomController.get_forms(args)
    except ApiException as err:
        return process_error(err)

    # 4. Render the response
    return render_template(
        "rooms/eg004_add_forms_to_room.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg004_add_forms_to_room.py",
        rooms=rooms,
        forms=forms
    )

"""Example 004: Adding forms to a room"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ...ds_config import DS_CONFIG
from ..examples.eg004_add_forms_to_room import Eg004AddFormsToRoomController
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error

example_number = 4
eg = f"eg00{example_number}"  # reference (and URL) for this example
eg004 = Blueprint(eg, __name__)


@eg004.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def add_form_to_room():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show room document
    """
    example = get_example_by_number(session["manifest"], example_number)

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
        title="Add a form to a room",
        h1="The DocuSign form was successfully added to the room",
        message="Results from the Rooms::AddFormToRoom method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg004.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["rooms_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get rooms
    3. Get forms
    4. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

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
        "eg004_add_forms_to_room.html",
        title="Adding forms to a room",
        source_file= "eg004_add_forms_to_room.py",
        rooms=rooms,
        forms=forms
    )

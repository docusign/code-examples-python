"""Example 006: Creating an external form fill session"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, Blueprint

from .eg006_create_external_form_fill_session import Eg006CreateExternalFormFillSessionController
from app.docusign import authenticate
from app.error_handlers import process_error

eg = "eg006"  # reference (and URL) for this example
eg006 = Blueprint("eg006", __name__)


@eg006.route("/eg006", methods=["POST"])
@authenticate(eg=eg)
def create_external_form_fill_session():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show URL for a new external form fill session
    """
    # 1. Get required arguments
    args = Eg006CreateExternalFormFillSessionController.get_args()

    try:
        # 2. Call the worker method
        results = Eg006CreateExternalFormFillSessionController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Show URL for a new external form fill session
    return render_template(
        "example_done.html",
        title="Create an external form fill session",
        h1="URL for a new external form fill session",
        message="Results from the Forms::CreateExternalFormFillSession:",
        json=json.dumps(json.dumps(results.to_dict(), default=str)),
        link=results.url,
        link_text="Please fill the form"
    )


@eg006.route("/eg006", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get rooms
    3. Render the response
    """
    # 1. Get required arguments
    args = Eg006CreateExternalFormFillSessionController.get_args()

    try:
        # 2. Get rooms
        rooms = Eg006CreateExternalFormFillSessionController.get_rooms(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "eg006_create_external_form_fill_session.html",
        title="Create an external form fill session",
        source_file=path.basename(path.dirname(__file__)) + "/eg006_create_external_form_fill_session.py",
        rooms=rooms,
    )


@eg006.route("/forms", methods=["POST"])
@authenticate(eg=eg)
def get_forms():
    """
    1. Get required arguments
    2. Get forms
    3. Get room name
    4. Render the response
    """
    # 1. Get required arguments
    args = Eg006CreateExternalFormFillSessionController.get_args()
    try:
        # 2. Get forms
        forms = Eg006CreateExternalFormFillSessionController.get_forms(args)

        # 3. Get room name
        room = Eg006CreateExternalFormFillSessionController.get_room(args)
    except ApiException as err:
        return process_error(err)

    # 4. Render the response
    return render_template(
        "eg006_create_external_form_fill_session.html",
        title="Create an external form fill session",
        source_file=path.basename(path.dirname(__file__)) + "/eg006_create_external_form_fill_session.py",
        forms=forms,
        room_id=args["room_id"],
        room_name=room.name
    )

"""Example 004: Adding forms to a room"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, Blueprint

from .controller import Eg004Controller
from app.docusign import authenticate
from app.error_handlers import process_error

eg = "eg004"  # reference (and url) for this example
eg004 = Blueprint("eg004", __name__)


@eg004.route("/eg004", methods=["POST"])
@authenticate(eg=eg)
def add_form_to_room():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show room document
    """
    # 1. Get required arguments
    args = Eg004Controller.get_args()

    try:
        # 2. Call the worker method
        results = Eg004Controller.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Show filtered rooms
    return render_template(
        "example_done.html",
        title="Add a form to a room",
        h1="The DocuSign Form was successfully added to the room",
        message="Results from the Rooms::AddFormToRoom method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@eg004.route("/eg004", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    1. Get required arguments
    2. Get rooms
    3. Get forms
    4. Render the response
    """
    # 1. Get required arguments
    args = Eg004Controller.get_args()

    try:
        # 2. Get rooms
        rooms = Eg004Controller.get_rooms(args)
        # 3. Get forms
        forms = Eg004Controller.get_forms(args)
    except ApiException as err:
        return process_error(err)

    # 4. Render the response
    return render_template(
        "eg004_add_forms_to_room.html",
        title="Adding forms to a room",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        rooms=rooms,
        forms=forms
    )

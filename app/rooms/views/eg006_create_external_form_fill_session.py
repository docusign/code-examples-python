"""Example 006: Creating an external form fill session"""

from os import path
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, redirect, Blueprint, session

from ...ds_config import DS_CONFIG
from ..examples.eg006_create_external_form_fill_session import Eg006CreateExternalFormFillSessionController
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 6
api = API_TYPE["ROOMS"]
eg = f"reg00{example_number}"  # reference (and URL) for this example
reg006 = Blueprint(eg, __name__)


@reg006.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_external_form_fill_session():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show URL for a new external form fill session
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg006CreateExternalFormFillSessionController.get_args()

    try:
        # 2. Call the worker method
        results = Eg006CreateExternalFormFillSessionController.worker(args)
    except ApiException as err:
        return process_error(err)
    
    #return results["redirect_url"]

    return render_template(
        "example_rooms_6_done.html",
        title=example["ExampleName"],
        json=json.dumps(json.dumps(results.to_dict(), default=str)),
        url = results.url
    )


@reg006.route(f"/{eg}", methods=["GET"])
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
    args = Eg006CreateExternalFormFillSessionController.get_args()

    try:
        # 2. Get rooms
        rooms = Eg006CreateExternalFormFillSessionController.get_rooms(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render the response
    return render_template(
        "rooms/eg006_create_external_form_fill_session.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg006_create_external_form_fill_session.py",
        rooms=rooms,
    )


@reg006.route("/forms", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_forms():
    """
    1. Get required arguments
    2. Get forms
    3. Get room name
    4. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

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
        "rooms/eg006_create_external_form_fill_session.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg006_create_external_form_fill_session.py",
        forms=forms,
        room_id=args["room_id"],
        room_name=room.name
    )

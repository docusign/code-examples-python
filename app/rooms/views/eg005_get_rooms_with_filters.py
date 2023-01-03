"""Example 005: Getting rooms with filters"""

from os import path
from datetime import datetime, timedelta
import json

from docusign_rooms.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ...ds_config import DS_CONFIG
from ..examples.eg005_get_rooms_with_filters import Eg005GetRoomsWithFiltersController
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ...consts import API_TYPE

example_number = 5
api = API_TYPE["ROOMS"]
eg = f"reg00{example_number}"  # reference (and URL) for this example
reg005 = Blueprint(eg, __name__)


@reg005.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_rooms_with_filters():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show filtered rooms
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg005GetRoomsWithFiltersController.get_args()

    try:
        # 2. Call the worker method
        results = Eg005GetRoomsWithFiltersController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 3. Show filtered rooms
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from the Rooms::GetRooms method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@reg005.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """
    1. Get required arguments
    2. Get room templates
    3. Set filtering parameters
    4. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg005GetRoomsWithFiltersController.get_args()

    try:
        # 2. Get room templates
        rooms = Eg005GetRoomsWithFiltersController.get_rooms(args)
    except ApiException as err:
        return process_error(err)

    # 3. Set filtering parameters
    start_date = datetime.today() - timedelta(days=10)
    end_date = datetime.today() + timedelta(days=1)

    # 4. Render the response
    return render_template(
        "rooms/eg005_get_rooms_with_filters.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg005_get_rooms_with_filters.py",
        rooms=rooms,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d")
    )

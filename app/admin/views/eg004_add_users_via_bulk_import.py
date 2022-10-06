"""Example 004: Add users via bulk import"""

import json
import os
from os import path
import time

from flask import Blueprint, render_template, request, Response, current_app, session
from docusign_admin.client.api_exception import ApiException

from app.error_handlers import process_error
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.ds_config import DS_CONFIG
from ..examples.eg004_add_users_via_bulk_import import Eg004AddUsersViaBulkImportController

example_number = 4
eg = f"eg00{example_number}"  # Reference(and URL) for this example
eg004 = Blueprint(eg, __name__)


@eg004.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def add_users_via_bulk_import():
    """
    1. Call the worker method
    2. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    controller = Eg004AddUsersViaBulkImportController()

    # 1. Call the worker method
    try:
        results = Eg004AddUsersViaBulkImportController.worker(controller, request)
        current_app.logger.info(f"Bulk import request ID: {results.id}")
    except ApiException as err:
        return process_error(err)
    
    # 2. Render the response
    return render_template(
        "example_done.html",
        check_status = True,
        title=example["ExampleName"],
        message=f"Results from UserImport:addBulkUserImport method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg004.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """
    Responds with the form for the example
    """
    example = get_example_by_number(session["manifest"], example_number)

    # Render the response
    return render_template(
        "eg004_add_users_via_bulk_import.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg004_add_users_via_bulk_import.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg004_add_users_via_bulk_import.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )

@eg004.route("/eg004examplecsv", methods=["GET"])
@authenticate(eg=eg)
def get_csv():
    """
    1. Creates an example of a CSV file
    2. Returns an example of a CSV file to the user
    """

    # 1. Creates an example of a CSV file
    csv_file = Eg004AddUsersViaBulkImportController.get_example_csv()

    # 2. Returns an example of a CSV file to the user
    return Response(
        csv_file,
        mimetype="text/csv",
        headers={
            "Content-disposition":"attachment; filename=bulk_import_demo.csv"
        }
    )

@eg004.route("/eg004check", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["admin_manifest_url"])
@authenticate(eg=eg)
def check_if_request_ready():
    """
    1. Checking if the request is complete
    2. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # Check if request is complete
    try:
        results = Eg004AddUsersViaBulkImportController.check_status()
    except ApiException as err:
        return process_error(err)

    if not results:
        return render_template(
            "eg004_file_state.html",
        )
    else:
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"Results from UserImport:getBulkUserImportRequest method:",
            json=json.dumps(json.dumps(results.to_dict(), default=str))
        )
    
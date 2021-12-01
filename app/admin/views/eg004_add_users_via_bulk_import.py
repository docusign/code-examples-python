"""Example 004: Add users via bulk import"""

import json
import os
from os import path
import time

from flask import Blueprint, render_template, request, Response, current_app
from docusign_admin.client.api_exception import ApiException

from app.error_handlers import process_error
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from .eg004_add_users_via_bulk_import import Eg004AddUsersViaBulkImportController


eg = "eg004"  # Reference(and URL) for this example
eg004 = Blueprint(eg, __name__)


@eg004.route("/eg004", methods=["POST"])
@authenticate(eg=eg)
def add_users_via_bulk_import():
    """
    1. Call the worker method
    2. Render the response
    """

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
        title="Add users via bulk import",
        h1="Add users via bulk import",
        message=f"Results from UserImport:addBulkUserImport method:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg004.route("/eg004", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    Responds with the form for the example
    """

    # Render the response
    return render_template(
        "eg004_add_users_via_bulk_import.html",
        title="Add users via bulk import",
        source_file=path.basename(path.dirname(__file__)) + "/eg004_add_users_via_bulk_import.py",
        source_url=(
            DS_CONFIG["admin_github_url"] +
            path.basename(path.dirname(__file__)) + "/eg004_add_users_via_bulk_import.py"
        ),
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
@authenticate(eg=eg)
def check_if_request_ready():
    """
    1. Checking if the request is complete
    2. Render the response
    """

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
            title="Add users via bulk import",
            h1="Add users via bulk import",
            message=f"Results from UserImport:getBulkUserImportRequest method:",
            json=json.dumps(json.dumps(results.to_dict(), default=str))
        )
    
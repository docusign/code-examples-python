"""Example 003: Bulk export user data"""

import json
import time
import os
from os import path
from pathlib import Path

from flask import Blueprint, render_template, Response, current_app, session
from docusign_admin.client.api_exception import ApiException

from app.error_handlers import process_error
from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.ds_config import DS_CONFIG
from ..examples.eg003_bulk_export_user_data import Eg003BulkExportUserDataController
from ...consts import API_TYPE

example_number = 3
api = API_TYPE["ADMIN"]
eg = f"aeg00{example_number}"  # Reference (and URL) for this example
aeg003 = Blueprint(eg, __name__)

@aeg003.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_user_list_data():
    """
    1. Call the worker method
    2. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Call the worker method
    try:
        results = Eg003BulkExportUserDataController.worker()
        current_app.logger.info(f"User list export ID: {results.id}")
    except ApiException as err:
        return process_error(err)

    csv_ready = False
    while csv_ready == False:
        csv_ready = check_if_csv_ready()
        time.sleep(5)

    if csv_ready == True:
        get_csv()

    file_path = Path("app/admin/examples/exported_user_data.csv").absolute()

    # 2. Render the response
    return render_template(
        "example_done.html",
        get_csv=True,
        title=example["ExampleName"],
        message=f"User data exported to {file_path}. </br> Results from UserExport:getUserListExport:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@aeg003.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """
    Responds with the form for the example
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # Render the response
    return render_template(
        "admin/eg003_bulk_export_user_data.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg003_bulk_export_user_data.py",
        source_url=DS_CONFIG["admin_github_url"] + "eg003_bulk_export_user_data.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )

def check_if_csv_ready():
    """
    1. Checking if a CSV file exists
    2. Render the response
    """

    # 1. Checking if a CSV file exists
    try:
        csv_file = Eg003BulkExportUserDataController.get_csv_user_list()
    except ApiException as err:
        return process_error(err)

    return bool(csv_file)

def get_csv():
    """
    1. Getting an existing CSV file
    2. Returns the finished csv file to the user
    """

    # 1. Getting an existing CSV file
    try:
        csv_file = Eg003BulkExportUserDataController.get_csv_user_list()
    except ApiException as err:
        return process_error(err)

    results_file = open("app/admin/examples/exported_user_data.csv", "w")
    results_file.write(csv_file)
    
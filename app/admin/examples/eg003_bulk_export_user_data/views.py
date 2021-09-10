"""Example 003: Bulk export user data"""

import json
import time
import os
from os import path
from pathlib import Path

from flask import Blueprint, render_template, Response, current_app
from docusign_admin.client.api_exception import ApiException

from app.error_handlers import process_error
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from .controller import Eg003Controller


eg = "eg003"  # Reference (and URL) for this example
eg003 = Blueprint(eg, __name__)

@eg003.route("/eg003", methods=["POST"])
@authenticate(eg=eg)
def get_user_list_data():
    """
    1. Call the worker method
    2. Render the response
    """

    # 1. Call the worker method
    try:
        results = Eg003Controller.worker()
        current_app.logger.info(f"User list export ID: {results.id}")
    except ApiException as err:
        return process_error(err)

    csv_ready = False
    while csv_ready == False:
        csv_ready = check_if_csv_ready()
        time.sleep(5)

    if csv_ready == True:
        get_csv()

    file_path = Path("app/admin/examples/eg003_bulk_export_user_data/exported_user_data.csv").absolute()

    # 2. Render the response
    return render_template(
        "example_done.html",
        get_csv=True,
        title="Bulk export user data",
        h1="Bulk export user data",
        message=f"User data exported to {file_path}. </br> Results from UserExport:getUserListExport:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg003.route("/eg003", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    Responds with the form for the example
    """

    # Render the response
    return render_template(
        "eg003_bulk_export_user_data.html",
        title="Bulk export user data",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=(
            DS_CONFIG["admin_github_url"] +
            path.basename(path.dirname(__file__)) + "/controller.py"
        ),
        documentation=DS_CONFIG["documentation"] + eg,
    )

def check_if_csv_ready():
    """
    1. Checking if a CSV file exists
    2. Render the response
    """

    # 1. Checking if a CSV file exists
    try:
        csv_file = Eg003Controller.get_csv_user_list()
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
        csv_file = Eg003Controller.get_csv_user_list()
    except ApiException as err:
        return process_error(err)

    results_file = open("app/admin/examples/eg003_bulk_export_user_data/exported_user_data.csv", "w")
    results_file.write(csv_file)
    
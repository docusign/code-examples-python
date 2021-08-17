"""Example 002: Bulk export user data"""

import json
from os import path

from flask import Blueprint, render_template, Response, current_app
from docusign_admin.client.api_exception import ApiException

from app.error_handlers import process_error
from app.docusign import authenticate
from app.ds_config import DS_CONFIG
from .controller import Eg002Controller


eg = "eg002"  # Reference (and URL) for this example
eg002 = Blueprint(eg, __name__)

@eg002.route("/eg002", methods=["POST"])
@authenticate(eg=eg)
def get_user_list_data():
    """
    1. Call the worker method
    2. Render the response
    """

    # 1. Call the worker method
    try:
        results = Eg002Controller.worker()
        current_app.logger.info(f"User list export ID: {results.id}")
    except ApiException as err:
        return process_error(err)

    # 2. Render the response
    return render_template(
        "example_done.html",
        get_csv=True,
        title="Bulk export user data",
        h1="Result of creating a bulk export user data",
        message="Results from UserExport:createUserListExport:",
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )

@eg002.route("/eg002", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """
    Responds with the form for the example
    """

    # Render the response
    return render_template(
        "eg002_bulk_export_user_data.html",
        title="Bulk export user data",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=(
            DS_CONFIG["admin_github_url"] +
            path.basename(path.dirname(__file__)) + "/controller.py"
        ),
        documentation=DS_CONFIG["documentation"] + eg,
    )

@eg002.route("/eg002check", methods=["GET"])
@authenticate(eg=eg)
def check_if_csv_ready():
    """
    1. Checking if a CSV file exists
    2. Render the response
    """

    # 1. Checking if a CSV file exists
    try:
        csv_file = Eg002Controller.get_csv_user_list()
    except ApiException as err:
        return process_error(err)

    # 2. Render the response
    return render_template(
        "eg002_file_state.html",
        get_csv=bool(csv_file)
    )

@eg002.route("/eg002csv", methods=["GET"])
@authenticate(eg=eg)
def get_csv():
    """
    1. Getting an existing CSV file
    2. Returns the finished csv file to the user
    """

    # 1. Getting an existing CSV file
    try:
        csv_file = Eg002Controller.get_csv_user_list()
    except ApiException as err:
        return process_error(err)

    # 2. Returns the finished csv file to the user
    return Response(
        csv_file,
        mimetype="text/csv",
        headers={
            "Content-disposition":"attachment; filename=user_list.csv"
        }
    )
    
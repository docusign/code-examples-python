"""Example 002: Post web query. """

import json
from os import path
from datetime import date, timedelta

from docusign_monitor.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app

from app.docusign import authenticate
from app.error_handlers import process_error
from ..examples.eg002_post_web_query import Eg002PostWebQueryController
from ...ds_config import DS_CONFIG

eg = "eg002"  # Reference (and URL) for this example
eg002 = Blueprint(eg, __name__)

@eg002.route(f"/{eg}", methods=["POST"])
@authenticate(eg=eg)
def get_monitoring_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    
    # 1. Get required arguments
    args = Eg002PostWebQueryController.get_args()
    try:
        # 2. Call the worker method
        results = Eg002PostWebQueryController.worker(args)
        current_app.logger.info(f"""Got your monitor data""")
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title="Query monitoring data with filters",
        h1="Query monitoring data with filters",
        message="Results from DataSet:postWebQuery method:",
        json=json.dumps(json.dumps(results.to_dict()))
    )

@eg002.route(f"/{eg}", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""

    current_date = date.today()
    start_date = date.today() - timedelta(10)

    return render_template(
        f"{eg}_post_web_query.html",
        title="Get monitoring data",
        source_file=f"{eg}_post_web_query.py",
        source_url=DS_CONFIG["monitor_github_url"] + f"{eg}_post_web_query.py",
        documentation=DS_CONFIG["documentation"] + eg,
        start_date=start_date,
        end_date=current_date
    )


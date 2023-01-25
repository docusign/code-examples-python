"""Example 002: Post web query. """

import json
from os import path
from datetime import date, timedelta

from docusign_monitor.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.error_handlers import process_error
from ..examples.eg002_post_web_query import Eg002PostWebQueryController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 2
api = API_TYPE["MONITOR"]
eg = f"meg00{example_number}"  # Reference (and URL) for this example
meg002 = Blueprint(eg, __name__)

@meg002.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_monitoring_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)
    
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
        title=example["ExampleName"],
        message="Results from DataSet:postWebQuery method:",
        json=json.dumps(json.dumps(results.to_dict()))
    )

@meg002.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    current_date = date.today()
    start_date = date.today() - timedelta(10)

    return render_template(
        f"monitor/eg002_post_web_query.html",
        title=example["ExampleName"],
        example=example,
        source_file=f"eg002_post_web_query.py",
        source_url=DS_CONFIG["monitor_github_url"] + f"eg002_post_web_query.py",
        documentation=DS_CONFIG["documentation"] + eg,
        start_date=start_date,
        end_date=current_date
    )


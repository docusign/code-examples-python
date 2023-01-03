"""Example 001: Get monitoring data. """

import json
from os import path

from docusign_monitor.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app, session

from app.docusign import authenticate, ensure_manifest, get_example_by_number
from app.error_handlers import process_error
from ..examples.eg001_get_monitoring_data import Eg001GetMonitoringDataController
from ...ds_config import DS_CONFIG
from ...consts import API_TYPE

example_number = 1
api = API_TYPE["MONITOR"]
eg = f"meg00{example_number}"  # Reference (and URL) for this example
meg001 = Blueprint(eg, __name__)

@meg001.route(f"/{eg}", methods=["POST"])
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
    args = Eg001GetMonitoringDataController.get_args()
    try:
        # 2. Call the worker method to get your monitor data
        results = Eg001GetMonitoringDataController.worker(args)
        current_app.logger.info(f"""Got your monitor data""")
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message="Results from DataSet:getStream method:",
        json=json.dumps(json.dumps(results, default=str))
    )

@meg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """ Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "monitor/eg001_get_monitoring_data.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg001_get_monitoring_data.py",
        source_url=DS_CONFIG["monitor_github_url"] + "eg001_get_monitoring_data.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


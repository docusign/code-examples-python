"""Example 001: Get monitoring data. """

import json
from os import path

from docusign_monitor.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app

from app.docusign import authenticate
from app.error_handlers import process_error
from .controller import Eg001Controller
from ....ds_config import DS_CONFIG

eg = "eg001"  # Reference (and URL) for this example
eg001 = Blueprint(eg, __name__)

@eg001.route("/eg001", methods=["POST"])
@authenticate(eg=eg)
def get_monitoring_data():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    
    # 1. Get required arguments
    args = Eg001Controller.get_args()
    try:
        # 2. Call the worker method to get your monitor data
        results = Eg001Controller.worker(args)
        current_app.logger.info(f"""Got your monitor data""")
    except ApiException as err:
        return process_error(err)

    return render_template(
        "example_done.html",
        title="Get monitoring data",
        h1="Monitoring data result",
        message="Results from DataSet:GetStreamForDataset method:",
        json=json.dumps(json.dumps(results, default=str))
    )

@eg001.route("/eg001", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """ Responds with the form for the example"""


    return render_template(
        "eg001_get_monitoring_data.html",
        title="Get monitoring data",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["monitor_github_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
    )


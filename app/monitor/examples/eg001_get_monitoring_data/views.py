"""Example 001: Get monitoring data. """

import json

from docusign_monitor.client.api_exception import ApiException
from flask import Blueprint, render_template, current_app

from app.docusign import authenticate
from app.error_handlers import process_error
from .controller import Eg001Controller

eg = "eg001"  # Reference (and URL) for this example
eg001 = Blueprint(eg, __name__)


@eg001.route("/eg001", methods=["GET"])
@authenticate(eg=eg)
def get_view():
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

    # 3. Render the response
    return render_template(
        "example_done.html",
        title="Get monitoring data",
        h1="Get monitoring data",
        json=json.dumps(json.dumps(results, default=str))
    )

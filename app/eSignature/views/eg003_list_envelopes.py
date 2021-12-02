"""Example 003: List envelopes in the user"s account"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, Blueprint

from ..examples.eg003_list_envelopes import Eg003ListEnvelopesController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg003"  # reference (and url) for this example
eg003 = Blueprint("eg003", __name__)


@eg003.route("/eg003", methods=["POST"])
@authenticate(eg=eg)
def envelope_list():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show envelopes
    """

    # 1. Get required arguments
    args = Eg003ListEnvelopesController.get_args()
    try:
        # 1. Call the worker method
        results = Eg003ListEnvelopesController.worker(args)
    except ApiException as err:
        return process_error(err)
    # 3. Show envelopes
    return render_template(
        "example_done.html",
        title="List envelopes results",
        h1="List envelopes results",
        message="Results from the Envelopes::listStatusChanges method:",
        json=json.dumps(json.dumps(results.to_dict()))
    )


@eg003.route("/eg003", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg003_list_envelopes.html",
        title="List changed envelopes",
        source_file=path.basename(path.dirname(__file__)) + "/eg003_list_envelopes.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg003_list_envelopes.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

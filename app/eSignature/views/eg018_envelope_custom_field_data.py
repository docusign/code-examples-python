"""018: Get an envelope"s custom field data"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg018_envelope_custom_field_data import Eg018EnvelopeCustomFieldDataController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg018"  # reference (and URL) for this example
eg018 = Blueprint("eg018", __name__)


@eg018.route("/eg018", methods=["POST"])
@authenticate(eg=eg)
def envelope_custom_field_data():
    """
    1. Get required args
    2. Call the worker method
    3. Show custom field data
    """

    if "envelope_id" in session:
        # 1. Get required args
        args = Eg018EnvelopeCustomFieldDataController.get_args()

        try:
            # 2. Call the worker method for creating envelope with custom field
            results = Eg018EnvelopeCustomFieldDataController.worker(args)
        except ApiException as err:
            return process_error(err)
        # 3. Step render the results
        return render_template(
            "example_done.html",
            title="Get custom field data",
            h1="Envelope custom field data",
            message="Results from the EnvelopeCustomFields::list method:",
            json=json.dumps(json.dumps(results.to_dict()))
        )
    else:
        return render_template(
            "eg018_envelope_custom_field_data.html",
            title="Envelope Custom Field Data",
            envelope_ok=False,
            source_file=path.basename(path.dirname(__file__)) + "/eg018_envelope_custom_field_data.py",
            source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg018_envelope_custom_field_data.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg018.route("/eg018", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg015_envelope_tab_data.html",
        title="Envelope information",
        envelope_ok="envelope_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/eg018_envelope_custom_field_data.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg018_envelope_custom_field_data.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

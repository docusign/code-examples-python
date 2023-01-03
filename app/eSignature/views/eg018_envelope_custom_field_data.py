"""018: Get an envelope"s custom field data"""

import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg018_envelope_custom_field_data import Eg018EnvelopeCustomFieldDataController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 18
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and URL) for this example
eg018 = Blueprint(eg, __name__)


@eg018.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def envelope_custom_field_data():
    """
    1. Get required args
    2. Call the worker method
    3. Show custom field data
    """
    example = get_example_by_number(session["manifest"], example_number, api)

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
            title=example["ExampleName"],
            message="Results from the EnvelopeCustomFields::list method:",
            json=json.dumps(json.dumps(results.to_dict()))
        )
    else:
        return render_template(
            "eSignature/eg018_envelope_custom_field_data.html",
            title=example["ExampleName"],
            example=example,
            envelope_ok=False,
            source_file= "eg018_envelope_custom_field_data.py",
            source_url=DS_CONFIG["github_example_url"] + "eg018_envelope_custom_field_data.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg018.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg015_envelope_tab_data.html",
        title=example["ExampleName"],
        example=example,
        envelope_ok="envelope_id" in session,
        source_file= "eg018_envelope_custom_field_data.py",
        source_url=DS_CONFIG["github_example_url"] + "eg018_envelope_custom_field_data.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

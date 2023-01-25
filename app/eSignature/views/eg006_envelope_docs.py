"""006: List an envelope"s documents"""
import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg006_envelope_docs import Eg006EnvelopeDocsController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 6
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg006 = Blueprint(eg, __name__)


@eg006.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def envelope_docs():
    """
    1. Get required arguments
    2. Call the worker method
    3. Save envelope documents
    4. Show envelope documents
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    if "envelope_id" in session:
        # 1. Get required arguments
        args = Eg006EnvelopeDocsController.get_args()
        try:
            # 2. Call the worker method
            results = Eg006EnvelopeDocsController.worker(args)
        except ApiException as err:
            return process_error(err)

        # 3. Save envelope documents
        Eg006EnvelopeDocsController.save_envelope_documents(results)

        # 4. Show envelope documents
        return render_template(
            "example_done.html",
            title="List an envelope's documents",
            h1="List an envelope's documents",
            message="Results from the EnvelopeDocuments::list method:",
            json=json.dumps(json.dumps(results.to_dict()))
        )

    else:
        return render_template(
            "eSignature/eg006_envelope_docs.html",
            title=example["ExampleName"],
            example=example,
            envelope_ok=False,
            source_file= "eg006_envelope_docs.py",
            source_url=DS_CONFIG["github_example_url"] + "eg006_envelope_docs.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg006.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg006_envelope_docs.html",
        title=example["ExampleName"],
        example=example,
        envelope_ok="envelope_id" in session,
        source_file= "eg006_envelope_docs.py",
        source_url=DS_CONFIG["github_example_url"] + "eg006_envelope_docs.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

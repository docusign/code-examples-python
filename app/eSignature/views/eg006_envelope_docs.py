"""006: List an envelope"s documents"""
import json
from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg006_envelope_docs import Eg006EnvelopeDocsController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg006"  # reference (and url) for this example
eg006 = Blueprint("eg006", __name__)


@eg006.route("/eg006", methods=["POST"])
@authenticate(eg=eg)
def envelope_docs():
    """
    1. Get required arguments
    2. Call the worker method
    3. Save envelope documents
    4. Show envelope documents
    """

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
            "eg006_envelope_docs.html",
            title="Envelope documents",
            envelope_ok=False,
            source_file= "eg006_envelope_docs.py",
            source_url=DS_CONFIG["github_example_url"] + "eg006_envelope_docs.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg006.route("/eg006", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg006_envelope_docs.html",
        title="Envelope documents",
        envelope_ok="envelope_id" in session,
        source_file= "eg006_envelope_docs.py",
        source_url=DS_CONFIG["github_example_url"] + "eg006_envelope_docs.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

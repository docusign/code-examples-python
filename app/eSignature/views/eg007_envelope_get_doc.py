"""007: Get an envelope"s document"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, send_file, Blueprint

from ..examples.eg007_envelope_get_doc import Eg007EnvelopeGetDocController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 7
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg007 = Blueprint(eg, __name__)


@eg007.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_envelope_doc():
    """
    1. Get required arguments
    2. Call the worker method
    3. Download envelope document
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    if "envelope_id" in session and "envelope_documents" in session:
        # 1. Get required arguments
        args = Eg007EnvelopeGetDocController.get_args()
        try:
            # 2. Call the worker method
            results = Eg007EnvelopeGetDocController.worker(args)
        except ApiException as err:
            return process_error(err)

        # 3. Download envelope document from the temp file path
        return send_file(
            results["data"],
            mimetype=results["mimetype"],
            as_attachment=True,
            attachment_filename=results["doc_name"]
        )
    else:
        return render_template(
            "eSignature/eg007_envelope_get_doc.html",
            title=example["ExampleName"],
            example=example,
            envelope_ok=False,
            documents_ok=False,
            source_file= "eg007_envelope_get_doc.py",
            source_url=DS_CONFIG["github_example_url"] + "eg007_envelope_get_doc.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg007.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    documents_ok = "envelope_documents" in session
    document_options = []
    if documents_ok:
        # Prepare the select items
        envelope_documents = session["envelope_documents"]
        document_options = map(lambda item:
                               {"text": item["name"], "document_id": item["document_id"]}
                               , envelope_documents["documents"])

    return render_template(
        "eSignature/eg007_envelope_get_doc.html",
        title=example["ExampleName"],
        example=example,
        envelope_ok="envelope_id" in session,
        documents_ok=documents_ok,
        source_file= "eg007_envelope_get_doc.py",
        source_url=DS_CONFIG["github_example_url"] + "eg007_envelope_get_doc.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        document_options=document_options
    )

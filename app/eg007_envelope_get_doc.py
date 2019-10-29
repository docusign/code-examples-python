"""007: Get an envelope's document"""

from flask import render_template, url_for, redirect, session, flash, request, send_file
from os import path
import json
import re
import io
from app import app, ds_config, views
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg007"  # reference (and url) for this example

def controller():
    """Controller router using the HTTP method"""
    if request.method == "GET":
        return get_controller()
    elif request.method == "POST":
        return create_controller()
    else:
        return render_template("404.html"), 404


def create_controller():
    """
    1. Check the token
    2. Call the worker method
    3. Show results
    """
    minimum_buffer_min = 3
    token_ok = views.ds_token_ok(minimum_buffer_min)
    if token_ok and "envelope_id" in session and "envelope_documents" in session:
        # 2. Call the worker method
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        pattern = re.compile("([^\w \-\@\.\,])+")
        document_id = pattern.sub("", request.form.get("document_id"))

        args = {
            "account_id": session["ds_account_id"],
            "envelope_id": session["envelope_id"],
            "base_path": session["ds_base_path"],
            "ds_access_token": session["ds_access_token"],
            "document_id": document_id,
            "envelope_documents": session["envelope_documents"]
        }

        try:
            results = worker(args)
        except ApiException as err:
            error_body_json = err and hasattr(err, "body") and err.body
            # we can pull the DocuSign error code and message from the response body
            error_body = json.loads(error_body_json)
            error_code = error_body and "errorCode" in error_body and error_body["errorCode"]
            error_message = error_body and "message" in error_body and error_body["message"]
            # In production, may want to provide customized error messages and
            # remediation advice to the user.
            return render_template("error.html",
                                   err=err,
                                   error_code=error_code,
                                   error_message=error_message
                                   )

        return send_file(
            results["data"],
            mimetype=results["mimetype"],
            as_attachment=True,
            attachment_filename=results["doc_name"]
        )

    elif not token_ok:
        flash("Sorry, you need to re-authenticate.")
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after
        # authentication.
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))
    elif not "envelope_id" in session or not "envelope_documents" in session:
        return render_template("eg007_envelope_get_doc.html",
                               title="Download an Envelope's Document",
                               envelope_ok=False,
                               documents_ok=False,
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               )


# ***DS.snippet.0.start
def worker(args):
    """
    1. Call the envelope get method
    """

    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args["base_path"]
    api_client.set_default_header("Authorization", "Bearer " + args["ds_access_token"])
    envelope_api = EnvelopesApi(api_client)
    document_id = args["document_id"]

    # The SDK always stores the received file as a temp file
    temp_file = envelope_api.get_document(args["account_id"], document_id, args["envelope_id"])
    doc_item = next(item for item in args["envelope_documents"]["documents"] if item["document_id"] == document_id)
    doc_name = doc_item["name"]
    has_pdf_suffix = doc_name[-4:].upper() == ".PDF"
    pdf_file = has_pdf_suffix
    # Add .pdf if it's a content or summary doc and doesn"t already end in .pdf
    if (doc_item["type"] == "content" or doc_item["type"] == "summary") and not has_pdf_suffix:
        doc_name += ".pdf"
        pdf_file = True
    # Add .zip as appropriate
    if doc_item["type"] == "zip":
        doc_name += ".zip"

    # Return the file information
    if pdf_file:
        mimetype = "application/pdf"
    elif doc_item["type"] == "zip":
        mimetype = "application/zip"
    else:
        mimetype = "application/octet-stream"

    return {"mimetype": mimetype, "doc_name": doc_name, "data": temp_file}
# ***DS.snippet.0.end

def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        documents_ok = "envelope_documents" in session
        document_options = []
        if documents_ok:
            # Prepare the select items
            envelope_documents = session["envelope_documents"]
            document_options = map( lambda item :
                {"text": item["name"], "document_id": item["document_id"]}
                , envelope_documents["documents"])

        return render_template("eg007_envelope_get_doc.html",
                               title="Download an Envelope's Document",
                               envelope_ok="envelope_id" in session,
                               documents_ok=documents_ok,
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               document_options=document_options
        )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


""" Example 010: Send binary docs with multipart mime: Remote signer, cc; the envelope has three documents"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views
import base64
import re
import json
import requests

eg = "eg010"  # reference (and url) for this example
demo_docs_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), "static/demo_documents"))


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
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):
        # 2. Call the worker method
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        pattern = re.compile("([^\w \-\@\.\,])+")
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name  = pattern.sub("", request.form.get("signer_name"))
        cc_email     = pattern.sub("", request.form.get("cc_email"))
        cc_name      = pattern.sub("", request.form.get("cc_name"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "cc_email": cc_email,
            "cc_name": cc_name,
            "status": "sent",
        }
        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "ds_access_token": session["ds_access_token"],
            "envelope_args": envelope_args
        }

        results = worker(args)

        if results["status_code"] < 299:
            # Success!
            return render_template("example_done.html",
                        title="Envelope sent",
                        h1="Envelope sent",
                        message=f"""The envelope has been created and sent!<br/>
                        Envelope ID {results["results"]["envelopeId"]}."""
            )
        else:
            # Problem!
            error_body = results["results"]
            # we can pull the DocuSign error code and message from the response body
            error_code = error_body and "errorCode" in error_body and error_body["errorCode"]
            error_message = error_body and "message" in error_body and error_body["message"]
            # In production, may want to provide customized error messages and
            # remediation advice to the user.
            return render_template("error.html",
                                   err=None,
                                   error_code=error_code,
                                   error_message=error_message
                                   )

    else:
        flash("Sorry, you need to re-authenticate.")
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after
        # authentication.
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


# ***DS.snippet.0.start
def worker(args):
    """
    This function does the work of creating the envelope by using
    the API directly with multipart mime
    @param {object} args An object with the following elements: <br/>
    <tt>account_id</tt>: Current account Id <br/>
    <tt> base_path</tt>: base path for making API call <br/>
    <tt> access_token</tt>: a valid access token <br/>
    <tt>demo_docs_path</tt>: relative path for the demo docs <br/> 
    <tt>envelope_args</tt>: envelopeArgs, an object with elements <br/> 
    <tt>signer_email</tt>, <tt>signer_name</tt>, <tt>cc_email</tt>, <tt>cc_name</tt>
    """

    # Step 1. Make the envelope JSON request body
    envelope_JSON = make_envelope_JSON( args["envelope_args"] )
    
    # Step 2. Gather documents and their headers
    # Read files 2 and 3 from a local directory
    # The reads could raise an exception if the file is not available!
    # Note: the fles are not binary encoded!
    with open(path.join(demo_docs_path, ds_config.DS_CONFIG["doc_docx"]), "rb") as file:
        doc2_docx_bytes = file.read()
    with open(path.join(demo_docs_path, ds_config.DS_CONFIG["doc_pdf"]), "rb") as file:
        doc3_pdf_bytes = file.read()

    documents = [
        {"mime": "text/html", "filename": envelope_JSON["documents"][0]["name"], 
         "document_id": envelope_JSON["documents"][0]["documentId"],
         "bytes": create_document1(args["envelope_args"]).encode("utf-8")},
        {"mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
         "filename": envelope_JSON["documents"][1]["name"], 
         "document_id": envelope_JSON["documents"][1]["documentId"],
         "bytes": doc2_docx_bytes},
        {"mime": "application/pdf", "filename": envelope_JSON["documents"][2]["name"], 
         "document_id": envelope_JSON["documents"][2]["documentId"],
         "bytes": doc3_pdf_bytes}
    ]

    # Step 3. Create the multipart body
    CRLF = b"\r\n"
    boundary = b"multipartboundary_multipartboundary"
    hyphens = b"--"

    req_body = b"".join([
        hyphens, boundary, 
        CRLF, b"Content-Type: application/json",
        CRLF, b"Content-Disposition: form-data",
        CRLF,
        CRLF, json.dumps(envelope_JSON, indent=4).encode("utf-8")])

    # Loop to add the documents.
    # See section Multipart Form Requests on page
    # https://developers.docusign.com/esign-rest-api/guides/requests-and-responses
    for d in documents:
        content_disposition = (f"Content-Disposition: file; filename={d['filename']};" +
                               f"documentid={d['document_id']}").encode("utf-8")
        req_body = b"".join([req_body,
            CRLF, hyphens, boundary,
            CRLF, f"Content-Type: {d['mime']}".encode("utf-8"),
            CRLF, content_disposition,
            CRLF,
            CRLF, d["bytes"]])
    
    # Add closing boundary
    req_body = b"".join([req_body, CRLF, hyphens, boundary, hyphens, CRLF])
    
    # Step 2. call Envelopes::create API method
    # Exceptions will be caught by the calling function
    results = requests.post(f"{args['base_path']}/v2/accounts/{args['account_id']}/envelopes",
        headers = {
            "Authorization": "bearer " + args["ds_access_token"],
            "Accept": "application/json",
            "Content-Type": f"multipart/form-data; boundary={boundary.decode('utf-8')}"
            },
        data = req_body
        )
    return {"status_code": results.status_code, "results": results.json()}


def make_envelope_JSON(args):
    """ 
    Create envelope JSON
    <br>Document 1: An HTML document.
    <br>Document 2: A Word .docx document.
    <br>Document 3: A PDF document.
    <br>DocuSign will convert all of the documents to the PDF format.
    <br>The recipients" field tags are placed using <b>anchor</b> strings.
    @param {Object} args parameters for the envelope:
      <tt>signerEmail</tt>, <tt>signerName</tt>, <tt>cc_email</tt>, <tt>cc_name</tt>
    @returns {Envelope} An envelope definition
    """

    # document 1 (html) has tag **signature_1**
    # document 2 (docx) has tag /sn1/
    # document 3 (pdf) has tag /sn1/
    #
    # The envelope has two recipients.
    # recipient 1 - signer
    # recipient 2 - cc
    # The envelope will be sent first to the signer.
    # After it is signed, a copy is sent to the cc person.

    # create the envelope definition
    env_json = {}
    env_json["emailSubject"] = "Please sign this document set"

    # add the documents
    doc1 = {
        "name": "Order acknowledgement", # can be different from actual file name
        "fileExtension": "html", # Source data format. Signed docs are always pdf.
        "documentId": "1" } # a label used to reference the doc
    doc2 = {
        "name": "Battle Plan", "fileExtension": "docx", "documentId": "2"}
    doc3 = {
        "name": "Lorem Ipsum", "fileExtension": "pdf", "documentId": "3"}
    # The order in the docs array determines the order in the envelope
    env_json["documents"] = [doc1, doc2, doc3]

    # create a signer recipient to sign the document, identified by name and email
    signer1 = {
        "email": args["signer_email"], "name": args["signer_name"],
        "recipientId": "1", "routingOrder": "1"}
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients.

    # create a cc recipient to receive a copy of the documents, identified by name and email
    cc1 = {
        "email": args["cc_email"], "name": args["cc_name"],
        "routingOrder": "2", "recipientId": "2"}

    # Create signHere fields (also known as tabs) on the documents,
    # We"re using anchor (autoPlace) positioning
    #
    # The DocuSign platform searches throughout your envelope"s
    # documents for matching anchor strings. So the
    # signHere2 tab will be used in both document 2 and 3 since they
    # use the same anchor string for their "signer 1" tabs.
    sign_here1 = {
        "anchorString": "**signature_1**", "anchorYOffset": "10", "anchorUnits": "pixels",
        "anchorXOffset": "20"}
    sign_here2 = {
        "anchorString": "/sn1/", "anchorYOffset": "10", "anchorUnits": "pixels",
        "anchorXOffset": "20"}

    # Tabs are set per recipient / signer
    signer1_tabs = {"signHereTabs": [sign_here1, sign_here2]}
    signer1["tabs"] = signer1_tabs

    # Add the recipients to the envelope object
    recipients = {"signers": [signer1], "carbonCopies": [cc1]}
    env_json["recipients"] = recipients

    # Request that the envelope be sent by setting |status| to "sent".
    # To request that the envelope be created as a draft, set to "created"
    env_json["status"] = "sent"

    return env_json


def create_document1(args):
    """ Creates document 1 -- an html document"""

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
          <meta charset="UTF-8">
        </head>
        <body style="font-family:sans-serif;margin-left:2em;">
        <h1 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
            color: darkblue;margin-bottom: 0;">World Wide Corp</h1>
        <h2 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
          margin-top: 0px;margin-bottom: 3.5em;font-size: 1em;
          color: darkblue;">Order Processing Division</h2>
        <h4>Ordered by {args['signer_name']}</h4>
        <p style="margin-top:0em; margin-bottom:0em;">Email: {args['signer_email']}</p>
        <p style="margin-top:0em; margin-bottom:0em;">Copy to: {args['cc_name']}, {args['cc_email']}</p>
        <p style="margin-top:3em;">
  Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. Donut jujubes oat cake jelly-o. Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
        </p>
        <!-- Note the anchor tag for the signature field is in white. -->
        <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
        </body>
    </html>
  """
# ***DS.snippet.0.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg010_send_binary_docs.html",
                               title="Send binary documents",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               signer_name=ds_config.DS_CONFIG["signer_name"],
                               signer_email=ds_config.DS_CONFIG["signer_email"]
        )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


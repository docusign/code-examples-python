import json
from os import path

import requests
from flask import request, session

from ...consts import demo_docs_path, pattern
from ...ds_config import DS_CONFIG


class Eg010SendBinaryDocsController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = pattern.sub("", request.form.get("cc_email"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
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
            "access_token": session["ds_access_token"],
            "envelope_args": envelope_args
        }
        return args

    @classmethod
    def worker(cls, args):
        """
        This function does the work of creating the envelope by using
        the API directly with multipart mime
        @param {object} args An object with the following args: <br/>
        <tt>account_id</tt>: Current account Id <br/>
        <tt> base_path</tt>: base path for making API call <br/>
        <tt> access_token</tt>: a valid access token <br/>
        <tt>demo_docs_path</tt>: relative path for the demo docs <br/>
        <tt>envelope_args</tt>: envelopeArgs, an object with elements <br/>
        <tt>signer_email</tt>, <tt>signer_name</tt>, <tt>cc_email</tt>, <tt>cc_name</tt>
        """

        # Step 1. Make the envelope JSON request body
        envelope_json = cls.make_envelope_json(args["envelope_args"])

        # Step 2. Gather documents and their headers
        # Read files 2 and 3 from a local directory
        # The reads could raise an exception if the file is not available!
        # Note: the fles are not binary encoded!
        with open(path.join(demo_docs_path, DS_CONFIG["doc_docx"]), "rb") as file:
            doc2_docx_bytes = file.read()
        with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
            doc3_pdf_bytes = file.read()

        documents = [
            {"mime": "text/html", "filename": envelope_json["documents"][0]["name"],
             "document_id": envelope_json["documents"][0]["documentId"],
             "bytes": cls.create_document1(args["envelope_args"]).encode("utf-8")},
            {"mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
             "filename": envelope_json["documents"][1]["name"],
             "document_id": envelope_json["documents"][1]["documentId"],
             "bytes": doc2_docx_bytes},
            {"mime": "application/pdf", "filename": envelope_json["documents"][2]["name"],
             "document_id": envelope_json["documents"][2]["documentId"],
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
            CRLF, json.dumps(envelope_json, indent=4).encode("utf-8")])

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
        headers = {
            "Authorization": "bearer " + args['access_token'],
            "Accept": "application/json",
            "Content-Type": f"multipart/form-data; boundary={boundary.decode('utf-8')}"
        }
        
        results = requests.post(
            url=f"{args['base_path']}/v2.1/accounts/{args['account_id']}/envelopes",
            headers=headers,
            data=req_body
        )
        return {"status_code": results.status_code, "results": results.json()}

    @classmethod
    def make_envelope_json(cls, args):
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
        env_json = {
            "emailSubject": "Please sign this document set"
        }
        # add the documents
        doc1 = {
            "name": "Order acknowledgement",  # can be different from actual file name
            "fileExtension": "html",  # Source data format. Signed docs are always pdf.
            "documentId": "1"}  # a label used to reference the doc
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

    @classmethod
    def create_document1(cls, args):
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
            <h4>Ordered by {args["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {args["signer_email"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {args["cc_name"]}, {args["cc_email"]}</p>
            <p style="margin-top:3em;">
                Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie.
                Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. 
                Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. 
                Donut jujubes oat cake jelly-o. 
                Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
            </p>
            <!-- Note the anchor tag for the signature field is in white. -->
            <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
            </body>
        </html>
      """

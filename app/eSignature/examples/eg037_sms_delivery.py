import base64
from os import path

from docusign_esign import (
    EnvelopesApi,
    EnvelopeDefinition,
    Document,
    Signer,
    CarbonCopy,
    SignHere,
    Tabs,
    Recipients,
    RecipientPhoneNumber
)

from flask import session, request

from ...consts import demo_docs_path, pattern
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg037SMSDeliveryController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""

        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
        cc_phone_number = request.form.get("cc_phone_number")
        cc_country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        country_code = request.form.get("country_code")
        delivery_method = request.form["delivery_method"]
        envelope_args = {
            "signer_name": signer_name,
            "status": "sent",
            "cc_name": cc_name,
            "country_code": country_code,
            "phone_number": phone_number,
            "cc_country_code" :cc_country_code,
            "cc_phone_number": cc_phone_number,
            "delivery_method": delivery_method
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
        1. Create the envelope request object
        2. Send the envelope
        """

        #ds-snippet-start:eSign37Step3
        envelope_args = args["envelope_args"]
        # Create the envelope request object
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        envelope_definition = cls.make_envelope(envelope_args)
        # Call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}
        #ds-snippet-end


    #ds-snippet-start:eSign37Step2
    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope:
        document 1 (HTML) has signHere anchor tag: **signature_1**
        document 2 (DOCX) has signHere anchor tag: /sn1/
        document 3 (PDF)  has signHere anchor tag: /sn1/
        DocuSign will convert all of the documents to the PDF format.
        The recipient’s field tags are placed using anchor strings.
        The envelope has two recipients:
        recipient 1: signer
        recipient 2: cc
        The envelope will be sent first to the signer via SMS.
        After it is signed, a copy is sent to the cc recipient via SMS.
        """
        # Create the envelope definition
        env = EnvelopeDefinition(
            email_subject="Please sign this document set"
        )
        doc1_b64 = base64.b64encode(bytes(cls.create_document1(args), "utf-8")).decode("ascii")
        # Read files 2 and 3 from a local folder
        # The reads could raise an exception if the file is not available!
        with open(path.join(demo_docs_path, DS_CONFIG["doc_docx"]), "rb") as file:
            doc2_docx_bytes = file.read()
        doc2_b64 = base64.b64encode(doc2_docx_bytes).decode("ascii")
        with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
            doc3_pdf_bytes = file.read()
        doc3_b64 = base64.b64encode(doc3_pdf_bytes).decode("ascii")

        # Create the document models
        document1 = Document(  # Create the DocuSign document object
            document_base64=doc1_b64,
            name="Order acknowledgement",  # Can be different from actual file name
            file_extension="html",  # Many different document types are accepted
            document_id="1"  # A label used to reference the doc
        )
        document2 = Document(  # Create the DocuSign document object
            document_base64=doc2_b64,
            name="Battle Plan",  # Can be different from actual file name
            file_extension="docx",  # Many different document types are accepted
            document_id="2"  # A label used to reference the doc
        )
        document3 = Document(  # Create the DocuSign document object
            document_base64=doc3_b64,
            name="Lorem Ipsum",  # Can be different from actual file name
            file_extension="pdf",  # Many different document types are accepted
            document_id="3"  # A label used to reference the doc
        )
        # The order in the docs array determines the order in the envelope
        env.documents = [document1, document2, document3]

        signerPhoneNumber = RecipientPhoneNumber(
            country_code=args["country_code"],
            number=args["phone_number"]
        )

        # Create the signer recipient model
        signer1 = Signer(
            name=args["signer_name"],
            recipient_id="1",
            routing_order="1",
            delivery_method=args["delivery_method"],
            phone_number=signerPhoneNumber
        )

        # Create a RecipientPhoneNumber and add it to the additional SMS notification
        ccPhoneNumber = RecipientPhoneNumber(
            country_code=args["cc_country_code"],
            number=args["cc_phone_number"]
        )

        # Create a cc recipient to receive a copy of the documents
        cc1 = CarbonCopy(
            name=args["cc_name"],
            recipient_id="2",
            routing_order="2",
            delivery_method=args["delivery_method"],
            phone_number=ccPhoneNumber
        )

        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients

        # Create signHere fields (also known as tabs) on the documents
        # We're using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope"s
        # documents for matching anchor strings. So the
        # signHere2 tab will be used in both document 2 and 3 since they
        # use the same anchor string for their "signer 1" tabs
        sign_here1 = SignHere(
            anchor_string="**signature_1**",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        sign_here2 = SignHere(
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        # Add the tabs model (including the SignHere tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1, sign_here2])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1], carbon_copies=[cc1])
        env.recipients = recipients

        # Request that the envelope be sent by setting status to "sent"
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]

        return env

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
            <p style="margin-top:0em; margin-bottom:0em;">Phone Number: {args["phone_number"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {args["cc_name"]}</p>
            <p style="margin-top:3em;">
                Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. 
                Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. 
                Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. 
                Donut jujubes oat cake jelly-o. 
                Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
            </p>
            <!-- Note the anchor tag for the signature field is in white -->
            <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
            </body>
        </html>
      """
#ds-snippet-end

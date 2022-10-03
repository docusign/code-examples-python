import base64
from os import path
from typing import List

from docusign_esign import (
    EnvelopesApi,
    Document,
    Signer,
    CarbonCopy,
    EnvelopeDefinition,
    SignHere,
    Tabs,
    Recipients,
)
from flask import session, request

from ...consts import demo_docs_path, pattern
from ...docusign import create_api_client


class Eg040DocumentVisibility:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        # 1. Parse request arguments
        signer1_email = pattern.sub("", request.form.get("signer1_email"))
        signer1_name = pattern.sub("", request.form.get("signer1_name"))
        signer2_email = pattern.sub("", request.form.get("signer2_email"))
        signer2_name = pattern.sub("", request.form.get("signer2_name"))
        cc_email = pattern.sub("", request.form.get("cc_email"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
        envelope_args = {
            "signer1_email": signer1_email,
            "signer1_name": signer1_name,
            "signer2_email": signer2_email,
            "signer2_name": signer2_name,
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
    def worker(cls, args, doc_docx_path, doc_pdf_path):
        """
        1. Create the envelope request object
        2. Send the envelope
        """
        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args, doc_docx_path, doc_pdf_path)
        
        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        # Step 2 start
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        # Step 2 end

        # Step 4 start
        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
        # Step 4 end
        
        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}
    
    @classmethod
    # Step 3 start
    def make_envelope(cls, args, doc_docx_path, doc_pdf_path):
        """
        Creates envelope
        args -- parameters for the envelope:
        signer_email, signer_name, signer_client_id
        returns an envelope definition
        """
        env = EnvelopeDefinition(
            email_subject = "Please sign this document set",
        )

        doc1_b64 = base64.b64encode(bytes(cls.create_document1(args), "utf-8")).decode("ascii")
        # read files 2 and 3 from a local directory
        # The reads could raise an exception if the file is not available!
        with open(path.join(demo_docs_path, doc_docx_path), "rb") as file:
            doc2_docx_bytes = file.read()
        doc2_b64 = base64.b64encode(doc2_docx_bytes).decode("ascii")
        with open(path.join(demo_docs_path, doc_pdf_path), "rb") as file:
            doc3_pdf_bytes = file.read()
        doc3_b64 = base64.b64encode(doc3_pdf_bytes).decode("ascii")

        # Create the document models
        document1 = Document(  # create the DocuSign document object
            document_base64=doc1_b64,
            name="Order acknowledgement",  # can be different from actual file name
            file_extension="html",  # many different document types are accepted
            document_id="1",  # a label used to reference the doc
        )
        document2 = Document(
            document_base64=doc2_b64,
            name="Battle Plan",  
            file_extension="docx",  
            document_id="2"  
        )
        document3 = Document(  
            document_base64=doc3_b64,
            name="Lorem Ipsum",  
            file_extension="pdf",  
            document_id="3" 
        )
        
        # The order in the docs array determines the order in the envelope
        env.documents = [document1, document2, document3]

        # Create the signer recipient model
        signer1 = Signer(
            # The signer1
            email=args["signer1_email"],
            name=args["signer1_name"],
            excluded_documents = ["2","3"], # Sets which documents are excluded for this signer
            recipient_id="1",
            routing_order="1",
            role_name="Signer1"
        )
        
        signer2 = Signer(
            # The signer2
            email=args["signer2_email"],
            name=args["signer2_name"],
            excluded_documents = ["1"],
            recipient_id="2",
            routing_order="1",
            role_name="Signer2"
        )

        cc = CarbonCopy(
            email=args["cc_email"],
            name=args["cc_name"],
            recipient_id="3",
            routing_order="2"
        )
        
        # Create signHere fields (also known as tabs) on the documents.
        sign_here1 = SignHere(
            document_id="1",
            page_number="1",
            name="Signer1",
            anchor_string="**signature_1**",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )
        sign_here2 = SignHere(
            document_id="2",
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )
        
        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(
            sign_here_tabs=[sign_here1, ],
        )
    
        signer2.tabs = Tabs(sign_here_tabs=[sign_here2, ])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1, signer2], carbon_copies=[cc])
        env.recipients = recipients

        # Request that the envelope be sent by setting |status| to "sent".
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
            <h4>Ordered by {args["signer1_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {args["signer1_email"]}</p>
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
    # Step 3 end

    # End

import base64
from os import path

from docusign_esign import EnvelopesApi, RecipientViewRequest, Document, Signer, EnvelopeDefinition, SignHere, Tabs, \
    Recipients, InPersonSigner
from flask import session, url_for, request

from ...consts import authentication_method, demo_docs_path, pattern, signer_client_id
from ...docusign import create_api_client, DSClient
from ...ds_config import DS_CONFIG


class Eg039InPersonSigner:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        # 1. Parse request arguments
        signer_name = pattern.sub("", request.form.get("signer_name"))
        envelope_args = {
            "host_email": session["ds_user_email"],
            "host_name": session["ds_user_name"],
            "signer_name": signer_name,
            "ds_return_url": url_for("ds.ds_return", _external=True),
        }
        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "envelope_args": envelope_args
        }
        return args

    @classmethod
    # Step 3 start
    def worker(cls, args):
        """
        1. Create the envelope request object
        2. Send the envelope
        3. Create the Recipient View request object
        4. Obtain the recipient_view_url for the embedded signing
        """
        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args)

        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id
        # Step 3 end

        # 3. Create the Recipient View request object
        # Step 4 start
        recipient_view_request = RecipientViewRequest(
            authentication_method=authentication_method,
            recipient_id="1",
            return_url=envelope_args["ds_return_url"],
            user_name=envelope_args["host_name"],
            email=envelope_args["host_email"]
        )
        # Step 4 end
        
        # Step 5 start
        # 4. Obtain the recipient_view_url for the embedded signing session
        # Exceptions will be caught by the calling function
        results = envelope_api.create_recipient_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request
        )
        # Step 5 end

        return {"envelope_id": envelope_id, "redirect_url": results.url}

    @classmethod
    # Step 2 start
    def make_envelope(cls, args):
        """
        Creates envelope
        args -- parameters for the envelope:
        signer_email, signer_name, signer_client_id
        returns an envelope definition
        """

        # document 1 (pdf) has tag /sn1/
        #
        # The envelope has one recipient.
        # recipient 1 - signer
        with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Create the document model
        document = Document(  # create the DocuSign document object
            document_base64=base64_file_content,
            name="Example document",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
            document_id=1  # a label used to reference the doc
        )

        # Create the in person signer recipient model
        signer = InPersonSigner(
            # The signer
            host_name = args["host_name"],
            host_email = args["host_email"],
            signer_name = args["signer_name"],
            recipient_id="1",
            routing_order="1",
        
        )

        # Create a sign_here tab (field on the document)
        sign_here = SignHere(
            # DocuSign SignHere field/tab
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        # Add the tabs model (including the sign_here tab) to the signer
        # The Tabs object wants arrays of the different field/tab types
        InPersonSigner.tabs = Tabs(sign_here_tabs=[sign_here])

        # Next, create the top level envelope definition and populate it.
        envelope_definition = EnvelopeDefinition(
            email_subject="Please host this in-person signing session",
            documents=[document],
            # The Recipients object wants arrays for each recipient type
            recipients=Recipients(in_person_signers=[signer]),
            status="sent"  # requests that the envelope be created and sent.
        )

        return envelope_definition
    # Step 2 end
    
    # End

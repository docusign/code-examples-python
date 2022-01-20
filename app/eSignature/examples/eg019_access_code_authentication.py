import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients
from flask import session, request

from ...consts import demo_docs_path, pattern
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg019AccessCodeAuthenticationController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        recip_access_code = request.form.get("accessCode")
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "status": "sent",
            "recip_access_code": recip_access_code
        }
        args = {
            "account_id": session["ds_account_id"],  # represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # represnts your {ACCESS_TOKEN}
            "envelope_args": envelope_args
        }
        return args

    @staticmethod
    def worker(args):
        """
        1. Create an api client
        2. Create an envelope definition object
        3. Call the eSignature REST API using the SDK
        """
        # Step 1: Construct your API headers
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        # Step 2: Construct your envelope
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document set"
        )

        # Open the example file
        with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Add a Document
        document1 = Document(  # create the DocuSign document object
            document_base64=base64_file_content,
            document_id="1",  # a label used to reference the doc
            file_extension="pdf",  # many different document types are accepted
            name="Lorem"  # can be different from actual file name
        )

        envelope_definition.documents = [document1]
        envelope_definition.status = args["envelope_args"]["status"]

        signer1 = Signer(
            email=args["envelope_args"]["signer_email"],  # represents your {signer_name}
            name=args["envelope_args"]["signer_name"],  # represents your {signer_email}
            access_code=args["envelope_args"]["recip_access_code"],
            # represents your {ACCESS_CODE} for your recipient to access the envelope
            recipient_id="1",
            routing_order="1"
        )

        # Create your signature tab
        sign_here1 = SignHere(
            name="SignHereTab",
            x_position="75",
            y_position="572",
            tab_label="SignHereTab",
            page_number="1",
            document_id="1",
            # A 1- to 8-digit integer or 32-character GUID to match recipient IDs on your own systems.
            # This value is referenced in the Tabs element below to assign tabs on a per-recipient basis.
            recipient_id="1"  # represents your {RECIPIENT_ID}
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1])

        # Tabs are set per recipient
        envelope_definition.recipients = Recipients(signers=[signer1])
        # Step 3: Call the eSignature REST API
        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        return results

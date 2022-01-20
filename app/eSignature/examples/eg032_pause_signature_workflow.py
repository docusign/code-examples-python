import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients
from docusign_esign.models import Workflow, WorkflowStep
from flask import session, request

from ...consts import demo_docs_path, pattern
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg032PauseSignatureWorkflowController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""

        # Strip anything other than characters listed
        signer1_email = pattern.sub("", request.form.get("signer1_email"))
        signer1_name = pattern.sub("", request.form.get("signer1_name"))
        signer2_email = pattern.sub("", request.form.get("signer2_email"))
        signer2_name = pattern.sub("", request.form.get("signer2_name"))
        envelope_args = {
            "signer1_email": signer1_email,
            "signer1_name": signer1_name,
            "signer2_email": signer2_email,
            "signer2_name": signer2_name,
            "status": "Sent",
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

        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args)
        api_client = create_api_client(
            base_path=args["base_path"], access_token=args["access_token"]
        )
        # 2. Call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(
            account_id=args["account_id"],
            envelope_definition=envelope_definition
        )

        return {"paused_envelope_id": results.envelope_id}

    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        Document: A txt document.
        DocuSign will convert document to the PDF format.
        """

        # The envelope has two recipients
        # Recipient 1 - signer1
        # Recipient 2 - signer2
        # The envelope will be sent first to the signer1
        # After it is signed, a signature workflow will be paused
        # After resuming (unpause) the signature workflow will send to the second recipient

        # Create the envelope definition
        env = EnvelopeDefinition(email_subject="EnvelopeWorkflowTest")

        # Read file from a local directory
        # The reads could raise an exception if the file is not available!
        with open(path.join(demo_docs_path, DS_CONFIG["doc_txt"]), "rb") as file:
            doc_docx_bytes = file.read()
        doc_b64 = base64.b64encode(doc_docx_bytes).decode("ascii")

        # Create the document model.
        document = Document(  # Create the DocuSign document object
            document_base64=doc_b64,
            name="Welcome",  # Can be different from actual file name
            file_extension="txt",  # Many different document types are accepted
            document_id="1"  # The label used to reference the doc
        )

        # The order in the docs array determines the order in the envelope.
        env.documents = [document, ]

        # Create the signer recipient models
        # routing_order (lower means earlier) determines the order of deliveries
        # to the recipients.
        signer1 = Signer(
            email=args["signer1_email"],
            name=args["signer1_name"],
            recipient_id="1",
            routing_order="1"
        )
        signer2 = Signer(
            email=args["signer2_email"],
            name=args["signer2_name"],
            recipient_id="2",
            routing_order="2"
        )

        # Create SignHere fields (also known as tabs) on the documents.
        sign_here1 = SignHere(
            document_id="1",
            page_number="1",
            tab_label="Sign Here",
            x_position="200",
            y_position="200"
        )

        sign_here2 = SignHere(
            document_id="1",
            page_number="1",
            tab_label="Sign Here",
            x_position="300",
            y_position="200"
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object takes arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1, ])
        signer2.tabs = Tabs(sign_here_tabs=[sign_here2, ])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1, signer2])
        env.recipients = recipients

        # Create a workflow model
        # Signature workflow will be paused after it is signed by the first signer
        workflow_step = WorkflowStep(
            action="pause_before",
            trigger_on_item="routing_order",
            item_id="2"
        )
        workflow = Workflow(workflow_steps=[workflow_step, ])
        # Add the workflow to the envelope object
        env.workflow = workflow

        # Request that the envelope be sent by setting |status| to "sent"
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]
        return env

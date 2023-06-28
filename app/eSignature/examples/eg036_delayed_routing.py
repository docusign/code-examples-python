import base64
from os import path

from docusign_esign import (
    EnvelopesApi,
    Envelope,
    EnvelopeDefinition,
    Document,
    Signer,
    SignHere,
    Tabs,
    Recipients,
    Workflow,
    DelayedRouting,
    EnvelopeDelayRule,
    WorkflowStep
)

from ...consts import demo_docs_path, pattern, signer_client_id
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG

class Eg036DelayedRoutingController:

    @classmethod
    def worker(cls, args):

        envelope_args = args["envelope_args"]
        envelope_definition = cls.make_envelope(envelope_args, DS_CONFIG["doc_docx"], DS_CONFIG["doc_pdf"])

        #ds-snippet-start:eSign36Step3
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
        #ds-snippet-end:eSign36Step3

        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}

    @classmethod
    def make_envelope(cls, args, doc_docx_path, doc_pdf_path):
        """
        Creates envelope
        Document 1: A PDF document.
        The recipients' field tags are placed using <b>anchor</b> strings.
        """

        # document 1 (PDF)  has sign here anchor tag /sn1/
        #
        # The envelope has two recipients.
        # recipient 1 - signer
        # recipient 2 - second signer
        # The envelope will be sent first to the signer.
        # After it is signed, there will be a delay before it is sent to the second signer.

        # create the envelope definition
        #ds-snippet-start:eSign36Step2
        env = EnvelopeDefinition(
            email_subject="Please sign this document"
        )
        
        with open(path.join(demo_docs_path, doc_pdf_path), "rb") as file:
            doc1_pdf_bytes = file.read()
        doc1_b64 = base64.b64encode(doc1_pdf_bytes).decode("ascii")

        # Create the document models
        document1 = Document(  # create the DocuSign document object
            document_base64=doc1_b64,
            name="Lorem Ipsum",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
            document_id="1"  # a label used to reference the doc
        )
        # The order in the docs array determines the order in the envelope
        env.documents = [document1]

        # Create the signer recipient model
        signer1 = Signer(
            email=args["signer_email"],
            name=args["signer_name"],
            recipient_id="1",
            routing_order="1"
        )
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients.

        # create a second recipient
        signer2 = Signer(
            email=args["signer_email2"],
            name=args["signer_name2"],
            recipient_id="2",
            routing_order="2"
        )

        # Create signHere fields (also known as tabs) on the documents,
        # We"re using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope"s
        # documents for matching anchor strings.

        sign_here1 = SignHere(
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )
        
        sign_here2 = SignHere(
            x_position = "320",
            y_position = "175",
            page_number = "1",
            document_id = "1"
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1])
        signer2.tabs = Tabs(sign_here_tabs=[sign_here2])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1, signer2])
        env.recipients = recipients

        delay = "0." + args["delay"] + ":00:00"

        workflow = Workflow()

        workflow_step = WorkflowStep()
        workflow_step.action = "pause_before"
        workflow_step.trigger_on_item = "routing_order"
        workflow_step.item_id = "2"
        delayed_routing = DelayedRouting(rules=[EnvelopeDelayRule(delay=delay)])
        workflow_step.delayed_routing = delayed_routing
        workflow.workflow_steps = [workflow_step]
        env.workflow = workflow

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]
        #ds-snippet-end:eSign36Step2

        return env
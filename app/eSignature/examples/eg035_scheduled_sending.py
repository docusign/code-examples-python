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
    ScheduledSending,
    EnvelopeDelayRule
)

from ...consts import demo_docs_path, pattern, signer_client_id
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg035ScheduledSendingController:

    @classmethod
    def worker(cls, args):
        envelope_args = args["envelope_args"]
        print("RESUMEDATE")
        print(envelope_args["resume_date"])
        envelope_definition = cls.make_envelope(envelope_args, DS_CONFIG["doc_docx"], DS_CONFIG["doc_pdf"])

        # Step 3 start
        #ds-snippet-start:eSign35Step3
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
        #ds-snippet-end:eSign35Step3
        # Step 3 end

        envelope_id = results.envelope_id

        print("ENVELOPE")
        print(envelope_id)

        return {"envelope_id": envelope_id}

    @classmethod
    def make_envelope(cls, args, doc_docx_path, doc_pdf_path):
        """
        Creates envelope
        Document 1: A PDF document.
        The recipients" field tags are placed using <b>anchor</b> strings.
        """

        # Step 2 start
        #ds-snippet-start:eSign35Step2
        # document 1 (PDF)  has sign here anchor tag /sn1/
        #
        # The envelope has one recipient.
        # recipient 1 - signer

        # create the envelope definition
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
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients.

        # Create signHere fields (also known as tabs) on the documents,
        # We're using anchor (autoPlace) positioning

        sign_here1 = SignHere(
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1])

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1])
        env.recipients = recipients

        workflow = Workflow()
        scheduled_sending_api_model = ScheduledSending()
        workflow.scheduled_sending = scheduled_sending_api_model

        envelope_delay_rule = EnvelopeDelayRule()
        envelope_delay_rule.resume_date = args["resume_date"] + "T00:00:00.000Z"
        workflow.scheduled_sending.rules = [envelope_delay_rule]
        env.workflow = workflow

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]
        #ds-snippet-end:eSign35Step2
        # Step 2 end

        return env

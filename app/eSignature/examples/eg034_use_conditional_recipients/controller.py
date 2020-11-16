import base64
from os import path

from docusign_esign import (
    Checkbox, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere,
    Tabs, Recipients
)
from docusign_esign.models import (
    ConditionalRecipientRule, ConditionalRecipientRuleCondition,
    ConditionalRecipientRuleFilter, RecipientGroup,
    RecipientOption, RecipientRouting, RecipientRules, Workflow, WorkflowStep
)
from flask import session, request

from ....consts import demo_docs_path, pattern
from ....docusign import create_api_client
from ....ds_config import DS_CONFIG


class Eg034Controller:
    @staticmethod
    def get_args():
        """Get request and session arguments"""

        # Strip anything other than characters listed
        signer1_email = pattern.sub("", request.form.get("signer1_email"))
        signer1_name = pattern.sub("", request.form.get("signer1_name"))
        signer_2a_email = pattern.sub("", request.form.get("signer_2a_email"))
        signer_2a_name = pattern.sub("", request.form.get("signer_2a_name"))
        signer_2b_email = pattern.sub("", request.form.get("signer_2b_email"))
        signer_2b_name = pattern.sub("", request.form.get("signer_2b_name"))
        envelope_args = {
            "signer1_email": signer1_email,
            "signer1_name": signer1_name,
            "signer_2a_email": signer_2a_email,
            "signer_2a_name": signer_2a_name,
            "signer_2b_email": signer_2b_email,
            "signer_2b_name": signer_2b_name,
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
        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(
            account_id=args["account_id"],
            envelope_definition=envelope_definition
        )

        return {"envelope_id": results.envelope_id}

    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        Document: A txt document.
        DocuSign will convert document to the PDF format.
        """

        # The envelope has two recipients.
        # recipient 1 - signer1
        # recipient 2 - signer2
        # The envelope will be sent first to the signer1.
        # After it is signed, a signature workflow will be paused.
        # After resuming (unpause) the signature workflow will send to the second recipient.

        # create the envelope definition
        env = EnvelopeDefinition(email_subject="ApproveIfChecked")

        # read file from a local directory
        # The reads could raise an exception if the file is not available!
        with open(path.join(demo_docs_path, DS_CONFIG["doc_txt"]),
                  "rb") as file:
            doc_docx_bytes = file.read()
        doc_b64 = base64.b64encode(doc_docx_bytes).decode("ascii")

        # Create the document model.
        document = Document(  # create the DocuSign document object
            document_base64=doc_b64,
            name="Welcome",  # can be different from actual file name
            file_extension="txt",  # many different document types are accepted
            document_id="1"  # a label used to reference the doc
        )

        # The order in the docs array determines the order in the envelope.
        env.documents = [document, ]

        # Create the signer model
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients.
        signer1 = Signer(
            email=args["signer1_email"],
            name=args["signer1_name"],
            recipient_id="1",
            routing_order="1",
            role_name="Purchaser"
        )
        # signer2 = Signer(
        #     email="gravecapa@gmail.com",
        #     name="Alpaca",
        #     recipient_id="2",
        #     routing_order="2",
        #     role_name="Approver"
        # )

        # Create signHere fields (also known as tabs) on the documents.
        sign_here1 = SignHere(
            document_id="1",
            page_number="1",
            name="SignHere",
            tab_label="PurchaserSignature",
            x_position="200",
            y_position="200"
        )
        sign_here2 = SignHere(
            document_id="1",
            page_number="1",
            name="SignHere",
            recipient_id="2",
            tab_label="ApproverSignature",
            x_position="300",
            y_position="200"
        )

        checkbox = Checkbox(
            document_id="1",
            page_number="1",
            name="ClickToApprove",
            selected="false",
            tab_label="ApproveWhenChecked",
            x_position="50",
            y_position="50"
        )
        #
        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(
            sign_here_tabs=[sign_here1, ],
            checkbox_tabs=[checkbox, ]
        )
        # signer2.tabs = Tabs(sign_here_tabs=[sign_here2, ])

        # Add the recipients to the envelope object
        env_recipients = Recipients(signers=[signer1, ])
        # recipients = Recipients(signers=[signer1, signer2])
        env.recipients = env_recipients

        # !!!!!!!! Create RecipientRouting model.
        signer_2a = RecipientOption(
            email=args["signer_2a_email"],
            name=args["signer_2a_name"],
            role_name="Signer when not checked",
            recipient_label="signer2a"
        )

        signer_2b = RecipientOption(
            email=args["signer_2b_email"],
            name=args["signer_2b_name"],
            role_name="Signer when checked",
            recipient_label="signer2b"
        )
        recipients = [signer_2a, signer_2b]
        recipient_group = RecipientGroup(
            group_name="Approver",
            group_message="Members of this group approve a workflow",
            recipients=recipients
        )

        filter1 = ConditionalRecipientRuleFilter(
            scope="tabs",
            recipient_id="1",
            tab_id="ApprovalTab",
            operator="equals",
            value="false",
            tab_label="ApproveWhenChecked"
        )
        filter2 = ConditionalRecipientRuleFilter(
            scope="tabs",
            recipient_id="1",
            tab_id="ApprovalTab",
            operator="equals",
            value="true",
            tab_label="ApproveWhenChecked"
        )

        condition1 = ConditionalRecipientRuleCondition(
            filters=[filter1, ],
            order="1",
            recipient_label="signer2a"
        )
        condition2 = ConditionalRecipientRuleCondition(
            filters=[filter2, ],
            order="2",
            recipient_label="signer2b"
        )
        conditions = [condition1, condition2]
        conditional_recipient = ConditionalRecipientRule(
            conditions=conditions,
            recipient_group=recipient_group,
            recipient_id="2",
            order="0",

        )
        rules = RecipientRules(conditional_recipients=[conditional_recipient, ])
        recipient_routing = RecipientRouting(rules=rules)

        # Create a workflow model.
        # Signature workflow will be paused after it is signed by the signer1.
        workflow_step = WorkflowStep(
            action="pause_before",
            trigger_on_item="routing_order",
            item_id="2",
            status="pending",
            recipient_routing=recipient_routing
        )

        workflow = Workflow(workflow_steps=[workflow_step, ])
        # Add the workflow to the envelope object
        env.workflow = workflow

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]
        return env

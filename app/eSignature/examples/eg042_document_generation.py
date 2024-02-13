import base64
from flask import session, request
from os import path
from docusign_esign import EnvelopesApi, TemplatesApi, EnvelopeDefinition, Document, Signer, SignHere, \
    DateSigned, Tabs, Recipients, DocGenFormField, EnvelopeTemplate, TemplateRole, DocGenFormFields, \
    DocGenFormFieldRequest, Envelope

from ...consts import demo_docs_path, pattern
from ...ds_config import DS_CONFIG
from ...docusign import create_api_client


class Eg042DocumentGenerationController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        envelope_args = {
            "candidate_email": pattern.sub("", request.form.get("candidate_email")),
            "candidate_name": pattern.sub("", request.form.get("candidate_name")),
            "manager_name": pattern.sub("", request.form.get("manager_name")),
            "job_title": pattern.sub("", request.form.get("job_title")),
            "salary": pattern.sub("", request.form.get("salary")),
            "start_date": pattern.sub("", request.form.get("start_date")),
            "doc_file": path.join(demo_docs_path, DS_CONFIG["doc_offer_letter"])
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
        1. Create the template
        2. Update template document
        3. Update recipient tabs
        4. Create draft envelope
        5. Get the document id
        6. Merge the data fields
        7. Send the envelope
        """

        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        templates_api = TemplatesApi(api_client)
        envelopes_api = EnvelopesApi(api_client)

        account_id = args["account_id"]
        envelope_args = args["envelope_args"]

        #ds-snippet-start:eSign42Step2
        template_data = cls.make_template()
        template = templates_api.create_template(account_id, envelope_template=template_data)
        template_id = template.template_id
        #ds-snippet-end:eSign42Step2

        # Update template document
        #ds-snippet-start:eSign42Step3
        document_id = '1'
        templates_api.update_document(
            account_id, document_id, template_id,
            envelope_definition=cls.template_document(envelope_args)
        )
        #ds-snippet-end:eSign42Step3

        # Update recipient tabs
        #ds-snippet-start:eSign42Step4
        recipient_id = '1'
        templates_api.create_tabs(
            account_id, recipient_id, template_id,
            template_tabs=cls.recipient_tabs()
        )
        #ds-snippet-end:eSign42Step4

        # Create draft envelope
        #ds-snippet-start:eSign42Step5
        envelope_definition = cls.make_envelope(template_id, envelope_args)
        envelope = envelopes_api.create_envelope(account_id, envelope_definition=envelope_definition)
        envelope_id = envelope.envelope_id
        #ds-snippet-end:eSign42Step5

        # Get the document id
        #ds-snippet-start:eSign42Step6
        doc_gen_form_fields_response = envelopes_api.get_envelope_doc_gen_form_fields(account_id, envelope_id)
        document_id_guid = doc_gen_form_fields_response.doc_gen_form_fields[0].document_id
        #ds-snippet-end:eSign42Step6

        # Merge the data fields
        #ds-snippet-start:eSign42Step7
        form_fields = cls.form_fields(envelope_args, document_id_guid)
        envelopes_api.update_envelope_doc_gen_form_fields(
            account_id,
            envelope_id,
            doc_gen_form_field_request=form_fields
        )
        #ds-snippet-end:eSign42Step7

        # Send the envelope
        #ds-snippet-start:eSign42Step8
        send_envelope_req = Envelope(status="sent")
        envelope = envelopes_api.update(account_id, envelope_id, envelope=send_envelope_req)
        #ds-snippet-end:eSign42Step8
        return envelope

    #ds-snippet-start:eSign42Step2
    @classmethod
    def make_template(cls):
        # Create recipient
        signer = Signer(
            role_name="signer",
            recipient_id="1",
            routing_order="1",
        )
        recipients = Recipients(
            signers=[signer]
        )

        # Create the envelope template model
        template_request = EnvelopeTemplate(
            name="Example document generation template",
            description="Example template created via the API",
            email_subject="Please sign this document",
            shared="false",
            recipients=recipients,
            status="created"
        )
        return template_request

    #ds-snippet-end:eSign42Step2

    #ds-snippet-start:eSign42Step3
    @classmethod
    def template_document(cls, args):
        with open(args["doc_file"], "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Create the document model
        document = Document(
            document_base64=base64_file_content,
            name="OfferLetterDemo.docx",
            file_extension="docx",
            document_id=1,
            order=1,
            pages=1
        )

        envelope_definition = EnvelopeDefinition(
            documents=[document]
        )
        return envelope_definition
    #ds-snippet-end:eSign42Step3

    #ds-snippet-start:eSign42Step4
    @classmethod
    def recipient_tabs(cls):
        # Create tabs
        sign_here = SignHere(
            anchor_string="Employee Signature",
            anchor_units="pixels",
            anchor_x_offset="5",
            anchor_y_offset="-22"
        )
        date_signed = DateSigned(
            anchor_string="Date",
            anchor_units="pixels",
            anchor_y_offset="-22"
        )
        tabs = Tabs(
            sign_here_tabs=[sign_here],
            date_signed_tabs=[date_signed]
        )
        return tabs
    #ds-snippet-end:eSign42Step4

    #ds-snippet-start:eSign42Step5
    @classmethod
    def make_envelope(cls, template_id, args):
        # Create the signer model
        signer = TemplateRole(
            email=args["candidate_email"],
            name=args["candidate_name"],
            role_name="signer"
        )

        # Create the envelope model
        envelope_definition = EnvelopeDefinition(
            template_roles=[signer],
            status="created",
            template_id=template_id
        )
        return envelope_definition
    #ds-snippet-end:eSign42Step5

    #ds-snippet-start:eSign42Step7
    @classmethod
    def form_fields(cls, args, document_id_guid):
        doc_gen_form_field_request = DocGenFormFieldRequest(
            doc_gen_form_fields=[
                DocGenFormFields(
                    document_id=document_id_guid,
                    doc_gen_form_field_list=[
                        DocGenFormField(
                            name="Candidate_Name",
                            value=args["candidate_name"]
                        ),
                        DocGenFormField(
                            name="Manager_Name",
                            value=args["manager_name"]
                        ),
                        DocGenFormField(
                            name="Job_Title",
                            value=args["job_title"]
                        ),
                        DocGenFormField(
                            name="Salary",
                            value=args["salary"]
                        ),
                        DocGenFormField(
                            name="Start_Date",
                            value=args["start_date"]
                        )
                    ]
                )
            ]
        )
        return doc_gen_form_field_request
    #ds-snippet-end:eSign42Step7

import base64

from docusign_webforms import ApiClient, FormInstanceManagementApi, FormManagementApi, CreateInstanceRequestBody
from docusign_esign import Document, Signer, SignHere, Tabs, Recipients, TemplatesApi, Checkbox, DateSigned, \
    Text, EnvelopeTemplate

from ...docusign import create_api_client


class Eg002CreateRemoteInstance:
    @classmethod
    def create_web_form_template(cls, args):
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        templates_api = TemplatesApi(api_client)

        web_forms_templates = templates_api.list_templates(
            account_id=args["account_id"],
            search_text=args["template_name"]
        )

        if int(web_forms_templates.result_set_size) > 0:
            template_id = web_forms_templates.envelope_templates[0].template_id
        else:
            template_req_object = cls.make_web_forms_template(args)
            template = templates_api.create_template(
                account_id=args["account_id"],
                envelope_template=template_req_object
            )
            template_id = template.template_id

        return template_id

    @classmethod
    def create_web_form_instance(cls, form_id, args):
        #ds-snippet-start:WebForms2Step2
        api_client = ApiClient()
        api_client.host = args["base_path"]
        api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {args['access_token']}")
        #ds-snippet-end:WebForms2Step2

        #ds-snippet-start:WebForms2Step4
        web_form_values = {
            "PhoneNumber": "555-555-5555",
            "Yes": ["Yes"],
            "Company": "Tally",
            "JobTitle": "Programmer Writer"
        }
        recipient = {
            "roleName": "signer",
            "name": args["signer_name"],
            "email": args["signer_email"]
        }
        web_form_req_object = {
            "formValues": web_form_values,
            "recipients": [recipient],
            "sendOption": "now"
        }
        #ds-snippet-end:WebForms2Step4

        #ds-snippet-start:WebForms2Step5
        webforms_api = FormInstanceManagementApi(api_client)
        web_form = webforms_api.create_instance(args["account_id"], form_id, web_form_req_object)
        #ds-snippet-end:WebForms2Step5

        return web_form

    @classmethod
    def list_web_forms(cls, args):
        api_client = ApiClient()
        api_client.host = args["base_path"]
        api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {args['access_token']}")

        #ds-snippet-start:WebForms2Step3
        webforms_api = FormManagementApi(api_client)
        web_forms = webforms_api.list_forms(args["account_id"], search=args["form_name"])
        #ds-snippet-end:WebForms2Step3

        return web_forms

    @classmethod
    def make_web_forms_template(cls, args):
        with open(args["pdf_file"], "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Create the document model
        document = Document(  # create the DocuSign document object
            document_base64=base64_file_content,
            name="World_Wide_Web_Form",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
            document_id=1  # a label used to reference the doc
        )

        # Create the signer recipient model
        signer = Signer(role_name="signer", recipient_id="1", routing_order="1")
        # Create fields using absolute positioning
        # Create a sign_here tab (field on the document)
        sign_here = SignHere(
            document_id="1",
            tab_label="Signature",
            anchor_string="/SignHere/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )
        check = Checkbox(
            document_id="1",
            tab_label="Yes",
            anchor_string="/SMS/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )
        text1 = Text(
            document_id="1",
            tab_label="FullName",
            anchor_string="/FullName/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )
        text2 = Text(
            document_id="1",
            tab_label="PhoneNumber",
            anchor_string="/PhoneNumber/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )
        text3 = Text(
            document_id="1",
            tab_label="Company",
            anchor_string="/Company/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )
        text4 = Text(
            document_id="1",
            tab_label="JobTitle",
            anchor_string="/JobTitle/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )
        date_signed = DateSigned(
            document_id="1",
            tab_label="DateSigned",
            anchor_string="/Date/",
            anchor_units="pixels",
            anchor_x_offset="0",
            anchor_y_offset="0"
        )
        # Add the tabs model to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer.tabs = Tabs(
            sign_here_tabs=[sign_here],
            checkbox_tabs=[check],
            text_tabs=[text1, text2, text3, text4],
            date_signed=[date_signed]
        )

        # Top object:
        template_request = EnvelopeTemplate(
            documents=[document], email_subject="Please sign this document",
            recipients=Recipients(signers=[signer]),
            description="Example template created via the API",
            name=args["template_name"],
            shared="false",
            status="created"
        )

        return template_request

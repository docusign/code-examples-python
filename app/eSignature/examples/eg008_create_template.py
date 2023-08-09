import base64
from os import path

from docusign_esign import Document, Signer, CarbonCopy, SignHere, Tabs, Recipients, \
    TemplatesApi, Checkbox, List, ListItem, Numerical, Radio, RadioGroup, Text, EnvelopeTemplate
from flask import session

from ...consts import demo_docs_path, doc_file, template_name
from ...docusign import create_api_client


class Eg008CreateTemplateController:
    @staticmethod
    def get_args():
        """
        Get session arguments
        """
        return {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "template_args": {
                "doc_file": path.join(demo_docs_path, doc_file),
                "template_name": template_name
            }
        }

    @classmethod
    def worker(cls, args):
        """
        1. Check to see if the template already exists
        2. If not, create the template
        """
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        templates_api = TemplatesApi(api_client)
        # 1. call Templates::list API method
        # Exceptions will be caught by the calling function
        results = templates_api.list_templates(account_id=args["account_id"], search_text=template_name)
        created_new_template = False
        
        if int(results.result_set_size) > 0:
            
            template_id = results.envelope_templates[0].template_id
            results_template_name = results.envelope_templates[0].name
            
        else:

            # Template not found -- so create it
            # 2. create the template
            #ds-snippet-start:eSign8Step3
            template_req_object = cls.make_template_req(args["template_args"])
            res = templates_api.create_template(account_id=args["account_id"], envelope_template=template_req_object)
            #ds-snippet-end:eSign8Step3
            template_id = res.template_id
            results_template_name = res.name
            created_new_template = True

        return {
            
            "template_id": template_id,
            "template_name": results_template_name,
            "created_new_template": created_new_template
        }

    @classmethod
    #ds-snippet-start:eSign8Step2
    def make_template_req(cls, args):
        """Creates template req object"""

        # document 1 (pdf)
        #
        # The template has two recipient roles.
        # recipient 1 - signer
        # recipient 2 - cc
        with open(args["doc_file"], "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Create the document model
        document = Document(  # create the DocuSign document object
            document_base64=base64_file_content,
            name="Lorem Ipsum",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
            document_id=1  # a label used to reference the doc
        )

        # Create the signer recipient model
        signer = Signer(role_name="signer", recipient_id="1", routing_order="1")
        # create a cc recipient to receive a copy of the envelope (transaction)
        cc = CarbonCopy(role_name="cc", recipient_id="2", routing_order="2")
        # Create fields using absolute positioning
        # Create a sign_here tab (field on the document)
        sign_here = SignHere(document_id="1", page_number="1", x_position="191", y_position="148")
        check1 = Checkbox(
            document_id="1",
            page_number="1",
            x_position="75",
            y_position="417",
            tab_label="ckAuthorization"
        )
        check2 = Checkbox(
            document_id="1",
            page_number="1",
            x_position="75",
            y_position="447",
            tab_label="ckAuthentication"
        )
        check3 = Checkbox(
            document_id="1",
            page_number="1",
            x_position="75",
            y_position="478",
            tab_label="ckAgreement"
        )
        check4 = Checkbox(
            document_id="1",
            page_number="1",
            x_position="75",
            y_position="508",
            tab_label="ckAcknowledgement"
        )
        list1 = List(
            document_id="1",
            page_number="1",
            x_position="142",
            y_position="291",
            font="helvetica",
            font_size="size14",
            tab_label="list",
            required="false",
            list_items=[
                ListItem(text="Red", value="red"),
                ListItem(text="Orange", value="orange"),
                ListItem(text="Yellow", value="yellow"),
                ListItem(text="Green", value="green"),
                ListItem(text="Blue", value="blue"),
                ListItem(text="Indigo", value="indigo"),
                ListItem(text="Violet", value="violet")
            ]
        )
        numerical = Numerical(
            document_id="1",
            validation_type="Currency",
            page_number="1",
            x_position="163",
            y_position="260",
            font="helvetica",
            font_size="size14",
            tab_label="numericalCurrency",
            width="84",
            height="23",
            required="false"
        )
        radio_group = RadioGroup(
            document_id="1",
            group_name="radio1",
            radios=[
                Radio(
                    page_number="1", x_position="142", y_position="384",
                    value="white", required="false"
                ),
                Radio(
                    page_number="1", x_position="74", y_position="384",
                    value="red", required="false"
                ),
                Radio(
                    page_number="1", x_position="220", y_position="384",
                    value="blue", required="false"
                )
            ]
        )
        text = Text(
            document_id="1",
            page_number="1",
            x_position="153",
            y_position="230",
            font="helvetica",
            font_size="size14",
            tab_label="text",
            height="23",
            width="84",
            required="false"
        )
        # Add the tabs model to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer.tabs = Tabs(
            sign_here_tabs=[sign_here],
            checkbox_tabs=[check1, check2, check3, check4],
            list_tabs=[list1],
            numerical_tabs=[numerical],
            radio_group_tabs=[radio_group],
            text_tabs=[text]
        )

        # Top object:
        template_request = EnvelopeTemplate(
            documents=[document], email_subject="Please sign this document",
            recipients=Recipients(signers=[signer], carbon_copies=[cc]),
            description="Example template created via the API",
            name=args["template_name"],
            shared="false",
            status="created"
        )

        return template_request
    #ds-snippet-end:eSign8Step2

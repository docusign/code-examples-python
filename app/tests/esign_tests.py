import datetime
import unittest
import base64
import os
from docusign_esign import Document, Signer, EnvelopeDefinition, SignHere, Tabs, \
    Recipients, CarbonCopy, EnvelopeTemplate, Checkbox, List, ListItem, Text, Radio, RadioGroup, TemplateRole, \
    CompositeTemplate, ServerTemplate, InlineTemplate, CustomFields, TextCustomField, BulkSendingList, \
    BulkSendingCopyRecipient, BulkSendingCopy, Numerical, LocalePolicyTab

from app.eSignature.examples.eg001_embedded_signing import Eg001EmbeddedSigningController
from app.eSignature.examples.eg002_signing_via_email import Eg002SigningViaEmailController
from app.eSignature.examples.eg008_create_template import Eg008CreateTemplateController
from app.eSignature.examples.eg009_use_template import Eg009UseTemplateController
from app.eSignature.examples.eg013_add_doc_to_template import Eg013AddDocToTemplateController
from app.eSignature.examples.eg016_set_tab_values import Eg016SetTabValuesController
from app.eSignature.examples.eg024_permissions_creating import Eg024PermissionsCreatingController
from app.eSignature.examples.eg028_brand_creating import Eg028BrandCreatingController
from app.eSignature.examples.eg029_brands_apply_to_envelope import Eg029BrandsApplyToEnvelopeController
from app.eSignature.examples.eg031_bulk_send import Eg031BulkSendController
from .test_helper import TestHelper, CONFIG
from ..consts import settings


class Testing(unittest.TestCase):
    TEMPLATE_ID = ""
    BRAND_ID = ""

    @classmethod
    def setUpClass(cls):
        results = TestHelper.authenticate()

        cls.access_token = results["access_token"]
        cls.account_id = results["account_id"]
        cls.base_path = results["base_path"]

    def test_embedded_signing_worker(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "signer_client_id": CONFIG["signer_client_id"],
            "ds_return_url": CONFIG["return_url"],
            "doc_pdf": os.path.abspath(CONFIG["test_pdf_file"]),
        }
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "envelope_args": envelope_args
        }

        results = Eg001EmbeddedSigningController.worker(args)

        self.assertIsNotNone(results)
        self.assertIsNotNone(results["envelope_id"])
        self.assertIsNotNone(results["redirect_url"])

    def test_embedded_signing_make_envelope(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "signer_client_id": CONFIG["signer_client_id"],
            "ds_return_url": CONFIG["return_url"],
            "doc_pdf": os.path.abspath(CONFIG["test_pdf_file"])
        }

        base64_file_content = TestHelper.read_as_base64(CONFIG["test_pdf_file"])

        envelope = EnvelopeDefinition(
            email_subject="Please sign this document sent from the Python SDK",
            status="sent",
            recipients=Recipients(
                signers=[Signer(
                    email=CONFIG["signer_email"],
                    name=CONFIG["signer_name"],
                    recipient_id='1',
                    routing_order='1',
                    client_user_id=CONFIG["signer_client_id"],
                    tabs=Tabs(
                        sign_here_tabs=[SignHere(
                            anchor_string="/sn1/",
                            anchor_units="pixels",
                            anchor_y_offset="10",
                            anchor_x_offset="20"
                        )]
                    )
                )]
            ),
            documents=[Document(
                document_base64=base64_file_content,
                name="Example document",
                file_extension="pdf",
                document_id=1
            )]
        )

        results = Eg001EmbeddedSigningController.make_envelope(envelope_args)

        self.assertIsNotNone(results)
        self.assertEqual(results, envelope)

    def test_sign_via_email(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"],
            "status": "sent"
        }
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "envelope_args": envelope_args
        }

        results = Eg002SigningViaEmailController.worker(args, os.path.abspath(CONFIG["test_docx_file"]),
                                                        os.path.abspath(CONFIG["test_pdf_file"]))

        self.assertIsNotNone(results)
        self.assertIsNotNone(results["envelope_id"])

    def test_sign_via_email_make_envelope(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"],
            "status": "sent"
        }

        html_document = f"""
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
            <h4>Ordered by {CONFIG["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {CONFIG["signer_email"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {CONFIG["cc_name"]}, {CONFIG["cc_email"]}</p>
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

        expected = EnvelopeDefinition(
            email_subject="Please sign this document set",
            status="sent",
            documents=[
                Document(
                    document_base64=base64.b64encode(bytes(html_document, "utf-8")).decode("ascii"),
                    name="Order acknowledgement",
                    file_extension="html",
                    document_id="1"
                ),
                Document(
                    document_base64=TestHelper.read_as_base64(os.path.abspath(CONFIG["test_docx_file"])),
                    name="Battle Plan",
                    file_extension="docx",
                    document_id="2"
                ),
                Document(
                    document_base64=TestHelper.read_as_base64(os.path.abspath(CONFIG["test_pdf_file"])),
                    name="Lorem Ipsum",
                    file_extension="pdf",
                    document_id="3"
                )
            ],
            recipients=Recipients(
                signers=[Signer(
                    email=CONFIG["signer_email"],
                    name=CONFIG["signer_name"],
                    recipient_id="1",
                    routing_order="1",
                    tabs=Tabs(sign_here_tabs=[
                        SignHere(
                            anchor_string="**signature_1**",
                            anchor_units="pixels",
                            anchor_y_offset="10",
                            anchor_x_offset="20"
                        ),
                        SignHere(
                            anchor_string="/sn1/",
                            anchor_units="pixels",
                            anchor_y_offset="10",
                            anchor_x_offset="20"
                        )
                    ])
                )],
                carbon_copies=[CarbonCopy(
                    email=CONFIG["cc_email"],
                    name=CONFIG["cc_name"],
                    recipient_id="2",
                    routing_order="2"
                )]
            )
        )

        envelope = Eg002SigningViaEmailController.make_envelope(envelope_args, os.path.abspath(CONFIG["test_docx_file"]),
                                                                os.path.abspath(CONFIG["test_pdf_file"]))

        self.assertIsNotNone(envelope)
        self.assertEqual(envelope, expected)

    def test_sign_via_email_html_doc(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"]
        }

        expected = f"""
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
            <h4>Ordered by {CONFIG["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {CONFIG["signer_email"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {CONFIG["cc_name"]}, {CONFIG["cc_email"]}</p>
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

        document = Eg002SigningViaEmailController.create_document1(envelope_args)

        self.assertIsNotNone(document)
        self.assertEqual(document, expected)

    def test_create_template(self):
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "template_args": {
                "doc_file": os.path.abspath(CONFIG["test_template_pdf_file"]),
                "template_name": CONFIG["template_name"]
            }
        }

        result = Eg008CreateTemplateController.worker(args)
        Testing.TEMPLATE_ID = result["template_id"]

        self.assertIsNotNone(result)
        self.assertIsNotNone(result["template_id"])
        self.assertIsNotNone(result["template_name"])
        self.assertIsNotNone(result["created_new_template"])

    def test_create_template_make_template(self):
        template_args = {
            "doc_file": os.path.abspath(CONFIG["test_template_pdf_file"]),
            "template_name": CONFIG["template_name"]
        }
        
        expected = EnvelopeTemplate(
            documents=[Document(
                document_base64=TestHelper.read_as_base64(CONFIG["test_template_pdf_file"]),
                name="Lorem Ipsum",
                file_extension="pdf",
                document_id=1
            )],
            email_subject="Please sign this document",
            recipients=Recipients(
                signers=[Signer(
                    role_name="signer",
                    recipient_id="1",
                    routing_order="1",
                    tabs=Tabs(
                        sign_here_tabs=[SignHere(
                            document_id="1",
                            page_number="1",
                            x_position="191",
                            y_position="148"
                        )],
                        checkbox_tabs=[
                            Checkbox(
                                document_id="1",
                                page_number="1",
                                x_position="75",
                                y_position="417",
                                tab_label="ckAuthorization"
                            ),
                            Checkbox(
                                document_id="1",
                                page_number="1",
                                x_position="75",
                                y_position="447",
                                tab_label="ckAuthentication"
                            ),
                            Checkbox(
                                document_id="1",
                                page_number="1",
                                x_position="75",
                                y_position="478",
                                tab_label="ckAgreement"
                            ),
                            Checkbox(
                                document_id="1",
                                page_number="1",
                                x_position="75",
                                y_position="508",
                                tab_label="ckAcknowledgement"
                            )
                        ],
                        list_tabs=[List(
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
                        )],
                        numerical_tabs=[Numerical(
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
                        )],
                        radio_group_tabs=[RadioGroup(
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
                        )],
                        text_tabs=[Text(
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
                        )]
                    )
                )],
                carbon_copies=[CarbonCopy(
                    role_name="cc",
                    recipient_id="2",
                    routing_order="2"
                )]
            ),
            description="Example template created via the API",
            name=CONFIG["template_name"],
            shared="false",
            status="created"
        )

        template = Eg008CreateTemplateController.make_template_req(template_args)

        self.assertIsNotNone(template)
        self.assertEqual(template, expected)

    def test_use_template(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"],
            "template_id": Testing.TEMPLATE_ID
        }
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "envelope_args": envelope_args
        }

        result = Eg009UseTemplateController.worker(args)

        self.assertIsNotNone(result)
        self.assertIsNotNone(result["envelope_id"])

    def test_use_template_make_envelope(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"],
            "template_id": Testing.TEMPLATE_ID
        }

        expected = EnvelopeDefinition(
            status="sent",
            template_id=Testing.TEMPLATE_ID,
            template_roles=[
                TemplateRole(
                    email=CONFIG["signer_email"],
                    name=CONFIG["signer_name"],
                    role_name="signer"
                ),
                TemplateRole(
                    email=CONFIG["cc_email"],
                    name=CONFIG["cc_name"],
                    role_name="cc"
                )
            ]
        )

        result = Eg009UseTemplateController.make_envelope(envelope_args)

        self.assertIsNotNone(result)
        self.assertEqual(result, expected)

    def test_include_doc_to_template(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"],
            "template_id": Testing.TEMPLATE_ID,
            "signer_client_id": CONFIG["signer_client_id"],
            "item": CONFIG["item"],
            "quantity": CONFIG["quantity"],
            "ds_return_url": CONFIG["return_url"]
        }
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "envelope_args": envelope_args
        }

        result = Eg013AddDocToTemplateController.worker(args)

        self.assertIsNotNone(result)
        self.assertIsNotNone(result["envelope_id"])
        self.assertIsNotNone(result["redirect_url"])

    def test_include_doc_to_template_make_envelope(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"],
            "template_id": Testing.TEMPLATE_ID,
            "signer_client_id": CONFIG["signer_client_id"],
            "item": CONFIG["item"],
            "quantity": CONFIG["quantity"],
            "ds_return_url": CONFIG["return_url"]
        }

        html_doc = f"""
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
            <h4>Ordered by {CONFIG["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {CONFIG["signer_email"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {CONFIG["cc_name"]}, {CONFIG["cc_email"]}</p>
            <p style="margin-top:3em; margin-bottom:0em;">Item: <b>{CONFIG["item"]}</b>, quantity: <b>{CONFIG["quantity"]}</b> at market price.</p>
            <p style="margin-top:3em;">
      Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. Donut jujubes oat cake jelly-o. Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
            </p>
            <!-- Note the anchor tag for the signature field is in white. -->
            <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
            </body>
        </html>
      """

        expected = EnvelopeDefinition(
            status="sent",
            composite_templates=[
                CompositeTemplate(
                    composite_template_id="1",
                    server_templates=[
                        ServerTemplate(sequence="1", template_id=Testing.TEMPLATE_ID)
                    ],
                    inline_templates=[
                        InlineTemplate(
                            sequence="2",
                            recipients=Recipients(
                                carbon_copies=[CarbonCopy(
                                    email=CONFIG["cc_email"],
                                    name=CONFIG["cc_name"],
                                    role_name="cc",
                                    recipient_id="2"
                                )],
                                signers=[Signer(
                                    email=CONFIG["signer_email"],
                                    name=CONFIG["signer_name"],
                                    role_name="signer",
                                    recipient_id="1",
                                    client_user_id=CONFIG["signer_client_id"]
                                )]
                            ))
                    ]
                ),
                CompositeTemplate(
                    composite_template_id="2",
                    inline_templates=[
                        InlineTemplate(
                            sequence="1",
                            recipients=Recipients(
                                carbon_copies=[CarbonCopy(
                                    email=CONFIG["cc_email"],
                                    name=CONFIG["cc_name"],
                                    role_name="cc",
                                    recipient_id="2"
                                )],
                                signers=[Signer(
                                    email=CONFIG["signer_email"],
                                    name=CONFIG["signer_name"],
                                    role_name="signer",
                                    recipient_id="1",
                                    client_user_id=CONFIG["signer_client_id"],
                                    tabs=Tabs(
                                        sign_here_tabs=[SignHere(
                                            anchor_string="**signature_1**",
                                            anchor_y_offset="10",
                                            anchor_units="pixels",
                                            anchor_x_offset="20"
                                        )]
                                    )
                                )]
                            )
                        )
                    ],
                    document=Document(
                        document_base64=base64.b64encode(bytes(html_doc, "utf-8")).decode("ascii"),
                        name="Appendix 1--Sales order",
                        file_extension="html",
                        document_id="1"
                    )
                )
            ]
        )

        envelope = Eg013AddDocToTemplateController.make_envelope(envelope_args)

        self.assertIsNotNone(envelope)
        self.assertEqual(envelope, expected)

    def test_include_doc_to_template_html_doc(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "cc_email": CONFIG["cc_email"],
            "cc_name": CONFIG["cc_name"],
            "item": CONFIG["item"],
            "quantity": CONFIG["quantity"]
        }

        expected = f"""
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
            <h4>Ordered by {CONFIG["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {CONFIG["signer_email"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {CONFIG["cc_name"]}, {CONFIG["cc_email"]}</p>
            <p style="margin-top:3em; margin-bottom:0em;">Item: <b>{CONFIG["item"]}</b>, quantity: <b>{CONFIG["quantity"]}</b> at market price.</p>
            <p style="margin-top:3em;">
      Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. Donut jujubes oat cake jelly-o. Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
            </p>
            <!-- Note the anchor tag for the signature field is in white. -->
            <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
            </body>
        </html>
      """

        document = Eg013AddDocToTemplateController.create_document1(envelope_args)

        self.assertIsNotNone(document)
        self.assertEqual(document, expected)

    def test_set_tab_values(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "signer_client_id": CONFIG["signer_client_id"],
            "ds_return_url": CONFIG["return_url"],
            "doc_file": os.path.abspath(CONFIG["test_template_docx_file"])
        }
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "envelope_args": envelope_args
        }

        results = Eg016SetTabValuesController.worker(args)

        self.assertIsNotNone(results)
        self.assertIsNotNone(results["envelope_id"])
        self.assertIsNotNone(results["redirect_url"])

    def test_set_tab_values_make_envelope(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "signer_client_id": CONFIG["signer_client_id"],
            "ds_return_url": CONFIG["return_url"],
            "doc_file": os.path.abspath(CONFIG["test_template_docx_file"])
        }

        expected = EnvelopeDefinition(
            email_subject="Please sign this document sent from the Python SDK",
            documents=[Document(
                document_base64=TestHelper.read_as_base64(CONFIG["test_template_docx_file"]),
                name="Lorem Ipsum",
                file_extension="docx",
                document_id=1
            )],
            recipients=Recipients(
                signers=[Signer(
                    email=CONFIG["signer_email"],
                    name=CONFIG["signer_name"],
                    recipient_id="1",
                    routing_order="1",
                    client_user_id=CONFIG["signer_client_id"],
                    tabs=Tabs(
                        sign_here_tabs=[SignHere(
                            anchor_string="/sn1/",
                            anchor_units="pixels",
                            anchor_y_offset="10",
                            anchor_x_offset="20"
                        )],
                        text_tabs=[
                            Text(
                                anchor_string="/legal/", anchor_units="pixels",
                                anchor_y_offset="-9", anchor_x_offset="5",
                                font="helvetica", font_size="size11",
                                bold="true", value=CONFIG["signer_name"],
                                locked="false", tab_id="legal_name",
                                tab_label="Legal name"
                            ),
                            Text(
                                anchor_string="/familiar/", anchor_units="pixels",
                                anchor_y_offset="-9", anchor_x_offset="5",
                                font="helvetica", font_size="size11",
                                bold="true", value=CONFIG["signer_name"],
                                locked="false", tab_id="familar_name",
                                tab_label="Familiar name"
                            )
                        ],
                        numerical_tabs=[Numerical(
                            page_number="1",
                            document_id="1",
                            x_position="210",
                            y_position="235",
                            validation_type="Currency",
                            font="helvetica",
                            font_size="size11",
                            bold="true",
                            locked="false",
                            height="23",
                            tab_id="salary",
                            tab_label="Salary",
                            numerical_value="123000",
                            locale_policy=LocalePolicyTab(
                                culture_name="en-US",
                                currency_code="usd",
                                currency_positive_format="csym_1_comma_234_comma_567_period_89",
                                currency_negative_format="minus_csym_1_comma_234_comma_567_period_89",
                                use_long_currency_format="true"
                            )
                        )]
                    )
                )]
            ),
            custom_fields=CustomFields(
                text_custom_fields=[TextCustomField(
                    name="salary",
                    required="false",
                    show="true",
                    value=str(123000)
                )]
            ),
            status="sent"
        )

        envelope = Eg016SetTabValuesController.make_envelope(envelope_args)

        self.assertIsNotNone(envelope)
        self.assertEqual(envelope, expected)

    def test_create_permission_profile(self):
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "permission_profile_name": f"{CONFIG['permission_profile_name']}_{int(datetime.datetime.utcnow().timestamp())}",
            "settings": settings
        }

        results = Eg024PermissionsCreatingController.worker(args)

        self.assertIsNotNone(results)

    def test_create_brand(self):
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "brand_name": f"{CONFIG['brand_name']}_{int(datetime.datetime.utcnow().timestamp())}",
            "default_language": CONFIG['default_language']
        }

        result = Eg028BrandCreatingController.worker(args)

        self.assertIsNotNone(result)

    def test_apply_brand_to_envelope(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "brand_id": Testing.BRAND_ID,
            "doc_pdf": os.path.abspath(CONFIG["test_pdf_file"])
        }
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "envelope_args": envelope_args
        }

        result = Eg029BrandsApplyToEnvelopeController.worker(args)

        self.assertIsNotNone(result)

    def test_apply_brand_to_envelope_make_envelope(self):
        envelope_args = {
            "signer_email": CONFIG["signer_email"],
            "signer_name": CONFIG["signer_name"],
            "brand_id": Testing.BRAND_ID,
            "doc_pdf": os.path.abspath(CONFIG["test_pdf_file"])
        }

        result = Eg029BrandsApplyToEnvelopeController.make_envelope(envelope_args)

        self.assertIsNotNone(result)

    def test_apply_brand_to_envelope_get_brands(self):
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token
        }

        result = Eg029BrandsApplyToEnvelopeController.get_brands(args)

        self.assertIsNotNone(result)

    def test_bulk_send(self):
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "doc_pdf": os.path.abspath(CONFIG["test_pdf_file"]),
            "signers": [
                {
                    "signer_name": CONFIG["signer_name"],
                    "signer_email": CONFIG["signer_email"],
                    "cc_email": CONFIG["cc_email"],
                    "cc_name": CONFIG["cc_name"]
                },
                {
                    "signer_name": CONFIG["signer2_name"],
                    "signer_email": CONFIG["signer2_email"],
                    "cc_email": CONFIG["cc2_email"],
                    "cc_name": CONFIG["cc2_name"]
                }
            ]
        }

        result = Eg031BulkSendController.worker(args)

        self.assertIsNotNone(result)

    def test_bulk_send_create_bulk_sending_list(self):
        args = [
            {
                "signer_name": CONFIG["signer_name"],
                "signer_email": CONFIG["signer_email"],
                "cc_email": CONFIG["cc_email"],
                "cc_name": CONFIG["cc_name"]
            },
            {
                "signer_name": CONFIG["signer2_name"],
                "signer_email": CONFIG["signer2_email"],
                "cc_email": CONFIG["cc2_email"],
                "cc_name": CONFIG["cc2_name"]
            }
        ]

        expected = BulkSendingList(
            name="sample",
            bulk_copies=[
                BulkSendingCopy(
                    recipients=[
                        BulkSendingCopyRecipient(
                            role_name="signer",
                            tabs=[],
                            name=CONFIG["signer_name"],
                            email=CONFIG["signer_email"]
                        ),
                        BulkSendingCopyRecipient(
                            role_name="cc",
                            tabs=[],
                            name=CONFIG["cc_name"],
                            email=CONFIG["cc_email"]
                        )
                    ],
                    custom_fields=[]
                ),
                BulkSendingCopy(
                    recipients=[
                        BulkSendingCopyRecipient(
                            role_name="signer",
                            tabs=[],
                            name=CONFIG["signer2_name"],
                            email=CONFIG["signer2_email"]
                        ),
                        BulkSendingCopyRecipient(
                            role_name="cc",
                            tabs=[],
                            name=CONFIG["cc2_name"],
                            email=CONFIG["cc2_email"]
                        )
                    ],
                    custom_fields=[]
                )
            ]
        )

        results = Eg031BulkSendController.create_bulk_sending_list(args)

        self.assertIsNotNone(results)
        self.assertEqual(results, expected)

    def test_bulk_send_make_draft_envelope(self):
        args = os.path.abspath(CONFIG["test_pdf_file"])

        base64_file_content = TestHelper.read_as_base64(CONFIG["test_pdf_file"])

        expected = EnvelopeDefinition(
            email_subject="Please Sign",
            status="created",
            envelope_id_stamping="true",
            recipients=Recipients(
                signers=[
                    Signer(
                        name="Multi Bulk Recipient::signer",
                        email="multiBulkRecipients-signer@docusign.com",
                        role_name="signer",
                        note="",
                        routing_order="1",
                        status="created",
                        delivery_method="email",
                        recipient_id="2",
                        recipient_type="signer",
                        tabs=Tabs(
                            sign_here_tabs=[
                                SignHere(
                                    anchor_string="/sn1/",
                                    anchor_units="pixels",
                                    anchor_y_offset="10",
                                    anchor_x_offset="20",
                                    tab_label="RecipentTab"
                                )
                            ]
                        )
                    )
                ],
                carbon_copies=[
                    Signer(
                        name="Multi Bulk Recipient::cc",
                        email="multiBulkRecipients-cc@docusign.com",
                        role_name="cc",
                        note="",
                        routing_order="2",
                        status="created",
                        delivery_method="email",
                        recipient_id="1",
                        recipient_type="signer"
                    )
                ]
            ),
            documents=[Document(
                document_base64=base64_file_content,
                name="lorem",
                file_extension="pdf",
                document_id=2
            )]
        )

        results = Eg031BulkSendController.make_draft_envelope(args)

        self.assertIsNotNone(results)
        self.assertEqual(results, expected)


if __name__ == '__main__':
    unittest.main()

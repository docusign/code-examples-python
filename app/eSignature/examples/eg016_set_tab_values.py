import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, \
    Numerical, LocalePolicyTab, CustomFields, TextCustomField, Text, RecipientViewRequest
from flask import current_app as app, session, url_for, request

from ...consts import demo_docs_path, authentication_method, signer_client_id, pattern
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg016SetTabValuesController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "signer_client_id": signer_client_id,
            "ds_return_url": url_for("ds.ds_return", _external=True),
            "doc_file": path.join(demo_docs_path, DS_CONFIG["doc_salary_docx"])
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
        3. Create the Recipient View request object
        4. Obtain the recipient_view_url for the embedded signing
        """
        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args)

        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        api_client = create_api_client(
            base_path=args["base_path"],
            access_token=args["access_token"]
        )

        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id

        # 3. Create the RecipientViewRequest object
        recipient_view_request = RecipientViewRequest(
            authentication_method=authentication_method,
            client_user_id=envelope_args["signer_client_id"],
            recipient_id="1",
            return_url=envelope_args["ds_return_url"],
            user_name=envelope_args["signer_name"], email=envelope_args["signer_email"]
        )
        # 4. Obtain the recipient view URL for the embedded signing
        # Exceptions will be caught by the calling function
        results = envelopes_api.create_recipient_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request
        )

        return {"envelope_id": envelope_id, "redirect_url": results.url}

    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        args -- parameters for the envelope:
        signer_email, signer_name, signer_client_id
        returns an envelope definition
        """

        # Document 1 (PDF) has tag /sn1/
        #
        # The envelope has one recipient:
        # recipient 1 - signer
        with open(args["doc_file"], "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Create the document model
        document = Document(  # Create the DocuSign document object
            document_base64=base64_file_content,
            name="Lorem Ipsum",  # Can be different from the actual filename
            file_extension="docx",  # Many different document types are accepted
            document_id=1  # A label used to reference the doc
        )

        # Create the signer recipient model
        signer = Signer(  # The signer
            email=args["signer_email"], name=args["signer_name"],
            recipient_id="1", routing_order="1",
            # Setting the client_user_id marks the signer as embedded
            client_user_id=args["signer_client_id"]
        )

        # Create a SignHere tab (field on the document)
        sign_here = SignHere(  # DocuSign SignHere field/tab
            anchor_string="/sn1/", anchor_units="pixels",
            anchor_y_offset="10", anchor_x_offset="20"
        )

        text_legal = Text(
            anchor_string="/legal/", anchor_units="pixels",
            anchor_y_offset="-9", anchor_x_offset="5",
            font="helvetica", font_size="size11",
            bold="true", value=args["signer_name"],
            locked="false", tab_id="legal_name",
            tab_label="Legal name")

        text_familar = Text(
            anchor_string="/familiar/", anchor_units="pixels",
            anchor_y_offset="-9", anchor_x_offset="5",
            font="helvetica", font_size="size11",
            bold="true", value=args["signer_name"],
            locked="false", tab_id="familar_name",
            tab_label="Familiar name")
        
        locale_policy_tab = LocalePolicyTab(
            culture_name="en-US",
            currency_code="usd",
            currency_positive_format="csym_1_comma_234_comma_567_period_89",
            currency_negative_format="minus_csym_1_comma_234_comma_567_period_89",
            use_long_currency_format="true"
        )

        numerical_salary = Numerical(
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
            locale_policy=locale_policy_tab

        )

        salary_custom_field = TextCustomField(
            name="salary",
            required="false",
            show="true",  # Yes, include in the CoC
            value=str(123000)
        )
        cf = CustomFields(text_custom_fields=[salary_custom_field])
        # Add the tabs model (including the SignHere tab) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer.tabs = Tabs(sign_here_tabs=[sign_here], text_tabs=[text_legal, text_familar], numerical_tabs=[numerical_salary])

        # Create the top level envelope definition and populate it
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document sent from the Python SDK",
            documents=[document],
            # The Recipients object wants arrays for each recipient type
            recipients=Recipients(signers=[signer]),
            custom_fields=cf,
            status="sent"  # Requests that the envelope be created and sent
        )

        return envelope_definition

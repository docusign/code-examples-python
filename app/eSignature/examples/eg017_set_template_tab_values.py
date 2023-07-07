from docusign_esign import EnvelopesApi, EnvelopeDefinition, RecipientViewRequest, Tabs, TemplateRole, RadioGroup, \
    TextCustomField, Text, CustomFields, Checkbox, Radio, List
from flask import current_app as app, url_for, request
from flask import session

from ...consts import authentication_method, signer_client_id, pattern
from ...docusign import create_api_client


class Eg017SetTemplateTabValuesController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = pattern.sub("", request.form.get("cc_email"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "signer_client_id": signer_client_id,
            "ds_return_url": url_for("ds.ds_return", _external=True),
            "cc_email": cc_email,
            "cc_name": cc_name
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
        # Create the envelope request object
        #ds-snippet-start:eSign17Step4
        envelope_definition = cls.make_envelope(envelope_args)
        #ds-snippet-end:eSign17Step4

        # Call Envelopes::create API method
        # Exceptions will be caught by the calling function
        
        #ds-snippet-start:eSign17Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign17Step2

        #ds-snippet-start:eSign17Step5
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id
        #ds-snippet-end:eSign17Step5
        app.logger.info(f"Envelope was created. EnvelopeId {envelope_id}")

        # Create the Recipient View request object
        #ds-snippet-start:eSign17Step6
        recipient_view_request = RecipientViewRequest(
            authentication_method=authentication_method,
            client_user_id=envelope_args["signer_client_id"],
            recipient_id="1",
            return_url=envelope_args["ds_return_url"],
            user_name=envelope_args["signer_name"], email=envelope_args["signer_email"]
        )
        # Obtain the recipient_view_url for the embedded signing
        # Exceptions will be caught by the calling function
        results = envelopes_api.create_recipient_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request
        )
        return {"envelope_id": envelope_id, "redirect_url": results.url}
        #ds-snippet-end:eSign17Step6

    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        args -- parameters for the envelope:
        signer_email, signer_name, signer_client_id
        returns an envelope definition
        """

        # Set the values for the fields in the template
        # List item
        #ds-snippet-start:eSign17Step3
        list1 = List(
            value="green", document_id="1",
            page_number="1", tab_label="list")

        # Checkboxes
        check1 = Checkbox(
            tab_label="ckAuthorization", selected="true")

        check3 = Checkbox(
            tab_label="ckAgreement", selected="true")

        radio_group = RadioGroup(
            group_name="radio1",
            radios=[Radio(value="white", selected="true")]
        )

        text = Text(
            tab_label="text", value="Jabberywocky!"
        )

        # We can also add a new tab (field) to the ones already in the template:
        text_extra = Text(
            document_id="1", page_number="1",
            x_position="280", y_position="172",
            font="helvetica", font_size="size14",
            tab_label="added text field", height="23",
            width="84", required="false",
            bold="true", value=args["signer_name"],
            locked="false", tab_id="name"
        )

        # Add the tabs model (including the SignHere tab) to the signer.
        # The Tabs object wants arrays of the different field/tab types
        # Tabs are set per recipient / signer
        tabs = Tabs(
            checkbox_tabs=[check1, check3], radio_group_tabs=[radio_group],
            text_tabs=[text, text_extra], list_tabs=[list1]
        )

        # create a signer recipient to sign the document, identified by name and email
        # We"re setting the parameters via the object creation
        signer = TemplateRole(  # The signer
            email=args["signer_email"], name=args["signer_name"],
            # Setting the client_user_id marks the signer as embedded
            client_user_id=args["signer_client_id"],
            role_name="signer",
            tabs=tabs
        )

        cc = TemplateRole(
            email=args["cc_email"],
            name=args["cc_name"],
            role_name="cc"
        )

        # create an envelope custom field to save our application"s
        # data about the envelope

        custom_field = TextCustomField(
            name="app metadata item",
            required="false",
            show="true",  # Yes, include in the CoC
            value="1234567"
        )

        cf = CustomFields(text_custom_fields=[custom_field])

        # Next, create the top level envelope definition and populate it.
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document sent from the Python SDK",
            # The Recipients object wants arrays for each recipient type
            template_id=session["template_id"],
            template_roles=[signer, cc],
            custom_fields=cf,
            status="sent"  # requests that the envelope be created and sent.
        )

        return envelope_definition
    #ds-snippet-end:eSign17Step3

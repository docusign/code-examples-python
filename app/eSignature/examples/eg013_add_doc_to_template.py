import base64

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, Recipients, \
    CompositeTemplate, InlineTemplate, ServerTemplate, RecipientViewRequest
from flask import url_for, session, request

from ...consts import signer_client_id, pattern
from ...docusign import create_api_client


class Eg013AddDocToTemplateController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = pattern.sub("", request.form.get("cc_email"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
        item = pattern.sub("", request.form.get("item"))
        quantity = pattern.sub("", request.form.get("quantity"))
        quantity = int(quantity)
        template_id = session["template_id"]
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "cc_email": cc_email,
            "cc_name": cc_name,
            "template_id": template_id,
            "signer_client_id": signer_client_id,
            "item": item,
            "quantity": quantity,
            "ds_return_url": url_for("ds.ds_return", _external=True)
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
        Create the envelope and the embedded signing
        1. Create the envelope request object using composite template to
           add the new document
        2. Send the envelope
        3. Make the recipient view request object
        4. Get the recipient view (embedded signing) url
        """
        envelope_args = args["envelope_args"]
        # 1. Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args)

        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
        envelope_id = results.envelope_id

        # 3. Create the Recipient View request object
        authentication_method = "None"  # How is this application authenticating
        # the signer? See the "authenticationMethod" definition
        # https://goo.gl/qUhGTm
        recipient_view_request = RecipientViewRequest(
            authentication_method=authentication_method,
            client_user_id=envelope_args["signer_client_id"],
            recipient_id="1",
            return_url=envelope_args["ds_return_url"],
            user_name=envelope_args["signer_name"],
            email=envelope_args["signer_email"]
        )
        # 4. Obtain the recipient_view_url for the embedded signing
        # Exceptions will be caught by the calling function
        results = envelope_api.create_recipient_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request
        )

        return {"envelope_id": envelope_id, "redirect_url": results.url}

    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        Uses compositing templates to add a new document to the existing template
        returns an envelope definition

        The envelope request object uses Composite Template to
        include in the envelope:
        1. A template stored on the DocuSign service
        2. An additional document which is a custom HTML source document
        """

        # 1. Create Recipients for server template. Note that Recipients object
        #    is used, not TemplateRole
        #
        # Create a signer recipient for the signer role of the server template
        signer1 = Signer(
            email=args["signer_email"],
            name=args["signer_name"],
            role_name="signer",
            recipient_id="1",
            # Adding clientUserId transforms the template recipient
            # into an embedded recipient:
            client_user_id=args["signer_client_id"]
        )
        # Create the cc recipient
        cc1 = CarbonCopy(
            email=args["cc_email"],
            name=args["cc_name"],
            role_name="cc",
            recipient_id="2"
        )
        # Recipients object:
        recipients_server_template = Recipients(
            carbon_copies=[cc1],
            signers=[signer1]
        )

        # 2. create a composite template for the Server template + roles
        comp_template1 = CompositeTemplate(
            composite_template_id="1",
            server_templates=[
                ServerTemplate(sequence="1", template_id=args["template_id"])
            ],
            # Add the roles via an inlineTemplate
            inline_templates=[
                InlineTemplate(sequence="2",
                               recipients=recipients_server_template)
            ]
        )

        # Next, create the second composite template that will
        # include the new document.
        #
        # 3. Create the signer recipient for the added document
        #    starting with the tab definition:
        sign_here1 = SignHere(
            anchor_string="**signature_1**",
            anchor_y_offset="10",
            anchor_units="pixels",
            anchor_x_offset="20"
        )
        signer1_tabs = Tabs(sign_here_tabs=[sign_here1])

        # 4. Create Signer definition for the added document
        signer1_added_doc = Signer(
            email=args["signer_email"],
            name=args["signer_name"],
            role_name="signer",
            recipient_id="1",
            client_user_id=args["signer_client_id"],
            tabs=signer1_tabs
        )
        # 5. The Recipients object for the added document.
        #    Using cc1 definition from above.
        recipients_added_doc = Recipients(
            carbon_copies=[cc1], signers=[signer1_added_doc])
        # 6. Create the HTML document that will be added to the envelope
        doc1_b64 = base64.b64encode(bytes(cls.create_document1(args), "utf-8")) \
            .decode("ascii")
        doc1 = Document(
            document_base64=doc1_b64,
            name="Appendix 1--Sales order",  # can be different from
            # actual file name
            file_extension="html",
            document_id="1"
        )
        # 6. create a composite template for the added document
        comp_template2 = CompositeTemplate(
            composite_template_id="2",
            # Add the recipients via an inlineTemplate
            inline_templates=[
                InlineTemplate(sequence="1", recipients=recipients_added_doc)
            ],
            document=doc1
        )
        # 7. create the envelope definition with the composited templates
        envelope_definition = EnvelopeDefinition(
            status="sent",
            composite_templates=[comp_template1, comp_template2]
        )

        return envelope_definition

    @classmethod
    def create_document1(cls, args):
        return f"""
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
            <h4>Ordered by {args["signer_name"]}</h4>
            <p style="margin-top:0em; margin-bottom:0em;">Email: {args["signer_email"]}</p>
            <p style="margin-top:0em; margin-bottom:0em;">Copy to: {args["cc_name"]}, {args["cc_email"]}</p>
            <p style="margin-top:3em; margin-bottom:0em;">Item: <b>{args["item"]}</b>, quantity: <b>{args["quantity"]}</b> at market price.</p>
            <p style="margin-top:3em;">
      Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. Donut jujubes oat cake jelly-o. Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
            </p>
            <!-- Note the anchor tag for the signature field is in white. -->
            <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
            </body>
        </html>
      """

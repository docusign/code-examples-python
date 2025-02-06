import base64
from os import path

from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, Notary, SignHere, Tabs, Recipients, \
    NotarySeal, NotaryRecipient, RecipientSignatureProvider, RecipientSignatureProviderOptions

from ...consts import demo_docs_path, pattern
from ...jwt_helpers import create_api_client


class Eg004SendWithThirdPartyNotary:

    @classmethod
    def worker(cls, args):
        """
        1. Create the envelope request object
        2. Send the envelope
        """

        envelope_args = args["envelope_args"]
        # Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args)
        #ds-snippet-start:Notary4Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        envelopes_api = EnvelopesApi(api_client)
        #ds-snippet-end:Notary4Step2

        #ds-snippet-start:Notary4Step4
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
        #ds-snippet-end:Notary4Step4

        envelope_id = results.envelope_id

        return {"envelope_id": envelope_id}

    #ds-snippet-start:Notary4Step3
    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        Document 1: An HTML document.
        DocuSign will convert all of the documents to the PDF format.
        The recipients" field tags are placed using <b>anchor</b> strings.
        """

        # document 1 (html) has sign here anchor tag **signature_1**
        #
        # The envelope has two recipients.
        # recipient 1 - signer
        # The envelope will be sent first to the signer.

        # create the envelope definition
        env = EnvelopeDefinition(
            email_subject="Please sign this document set"
        )
        doc1_b64 = base64.b64encode(bytes(cls.create_document1(args), "utf-8")).decode("ascii")

        # Create the document models
        document1 = Document(  # create the DocuSign document object
            document_base64=doc1_b64,
            name="Order acknowledgement",  # can be different from actual file name
            file_extension="html",  # many different document types are accepted
            document_id="1"  # a label used to reference the doc
        )
        # The order in the docs array determines the order in the envelope
        env.documents = [document1]

        # Create the signer recipient model
        signer1 = Signer(
            email=args["signer_email"],
            name=args["signer_name"],
            recipient_id="2",
            routing_order="1",
            client_user_id="1000",
            notary_id="1"
        )
        # routingOrder (lower means earlier) determines the order of deliveries
        # to the recipients. Parallel routing order is supported by using the
        # same integer as the order for two or more recipients.

        # Create signHere fields (also known as tabs) on the documents,
        # We"re using anchor (autoPlace) positioning
        #
        # The DocuSign platform searches throughout your envelope"s
        # documents for matching anchor strings. So the
        # signHere2 tab will be used in both document 2 and 3 since they
        # use the same anchor string for their "signer 1" tabs.
        sign_here1 = SignHere(
            document_id="1",
            x_position="200",
            y_position="235",
            page_number="1"
        )

        sign_here2 = SignHere(
            stamp_type="stamp",
            document_id="1",
            x_position="200",
            y_position="150",
            page_number="1"
            
        )

        # Add the tabs model (including the sign_here tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer1.tabs = Tabs(sign_here_tabs=[sign_here1, sign_here2])

        notary_seal_tab = NotarySeal(
            x_position = "300",
            y_position = "235",
            document_id = "1",
            page_number = "1",
        )

        notary_sign_here = SignHere(
            x_position = "300",
            y_position = "150",
            document_id = "1",
            page_number = "1",
        )

        notary_tabs = Tabs(
            sign_here_tabs = [notary_sign_here],
            notary_seal_tabs = [ notary_seal_tab ],
        )

        recipient_signature_provider = RecipientSignatureProvider(
            seal_documents_with_tabs_only = "false",
            signature_provider_name = "ds_authority_idv",
            signature_provider_options = RecipientSignatureProviderOptions()
        )

        notary_recipient = NotaryRecipient(
            name = "Notary",
            recipient_id = "1",
            routing_order = "1",
            tabs = notary_tabs,
            notary_type = "remote",
            notary_source_type = "thirdparty",
            notary_third_party_partner = "onenotary",
            recipient_signature_providers = [recipient_signature_provider]
        )

        # Add the recipients to the envelope object
        recipients = Recipients(signers=[signer1], notaries= [notary_recipient])
        env.recipients = recipients        

        # Request that the envelope be sent by setting |status| to "sent".
        # To request that the envelope be created as a draft, set to "created"
        env.status = args["status"]

        return env

    @classmethod
    def create_document1(cls, args):
        """ Creates document 1 -- an html document"""

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
        #ds-snippet-end:Notary4Step3

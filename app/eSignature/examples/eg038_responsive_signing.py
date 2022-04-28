from os import path

from docusign_esign import (
    EnvelopesApi,
    RecipientViewRequest,
    Document,
    Signer,
    CarbonCopy,
    EnvelopeDefinition,
    Recipients,
    DocumentHtmlDefinition
)
from flask import session, url_for, request

from ...consts import authentication_method, demo_docs_path, pattern, signer_client_id
from ...docusign import create_api_client


class Eg038ResponsiveSigning:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        # 1. Parse request arguments
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = pattern.sub("", request.form.get("cc_email"))
        cc_name = pattern.sub("", request.form.get("cc_name"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "cc_email": cc_email,
            "cc_name": cc_name,
            "signer_client_id": signer_client_id,
            "ds_return_url": url_for("ds.ds_return", _external=True),
            "doc_file": path.join(demo_docs_path, "order_form.html")
        }
        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "envelope_args": envelope_args
        }
        return args

    # Step 3 start
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
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id

        # 3. Create the Recipient View request object
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
    # Step 3 end

    # Step 2 start
    @classmethod
    def make_envelope(cls, args):
        """
        Creates envelope
        args -- parameters for the envelope:
        signer_email, signer_name, signer_client_id
        returns an envelope definition
        """

        html_definition = DocumentHtmlDefinition(
            source=cls.get_html_content(args)
        )

        # Create the document model
        document = Document(  # create the DocuSign document object
            html_definition=html_definition,
            name="doc1.html",  # can be different from actual file name
            document_id=1  # a label used to reference the doc
        )

        # Create the signer recipient model
        signer = Signer(
            # The signer
            email=args["signer_email"],
            name=args["signer_name"],
            recipient_id="1",
            routing_order="1",
            # Setting the client_user_id marks the signer as embedded
            client_user_id=args["signer_client_id"],
            role_name="Signer"
        )

        cc = CarbonCopy(
            email=args["cc_email"],
            name=args["cc_name"],
            recipient_id="2",
            routing_order="2"
        )

        # Next, create the top level envelope definition and populate it.
        envelope_definition = EnvelopeDefinition(
            email_subject="Example Signing Document",
            documents=[document],
            # The Recipients object wants arrays for each recipient type
            recipients=Recipients(signers=[signer], carbon_copies=[cc]),
            status="sent"  # requests that the envelope be created and sent.
        )

        return envelope_definition

    @classmethod
    def get_html_content(cls, args):
        with open(args["doc_file"], "r") as file:
            doc_html = file.read()

        return doc_html.replace("{signer_name}", args["signer_name"]) \
            .replace("{signer_email}", args["signer_email"]) \
            .replace("{cc_name}", args["cc_name"]) \
            .replace("{cc_email}", args["cc_email"]) \
            .replace("/sn1/", "<ds-signature data-ds-role=\"Signer\"/>") \
            .replace("/l1q/", "<input data-ds-type=\"number\"/>") \
            .replace("/l2q/", "<input data-ds-type=\"number\"/>")

# Step 2 end
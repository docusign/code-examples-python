import base64
from datetime import datetime as dt, timezone
from os import path

from docusign_esign import AccountsApi, EnvelopesApi, RecipientIdentityInputOption, RecipientIdentityPhoneNumber, RecipientViewRequest, Document, Signer, EnvelopeDefinition, \
    Recipients, RecipientIdentityVerification
from flask import session, url_for, request

from ...consts import demo_docs_path, pattern, signer_client_id
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg044FocusedViewController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        # 1. Parse request arguments
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        phone_number = pattern.sub("", request.form.get("phone_number", ""))
        country_code = pattern.sub("", request.form.get("country_code", ""))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "phone_number": phone_number if phone_number else None,
            "country_code": country_code if country_code else None,
            "signer_client_id": signer_client_id,
            "ds_return_url": url_for("ds.ds_return", _external=True),
            "ds_ping_url": DS_CONFIG["app_url"] + "/",
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
        #ds-snippet-start:eSign44Step3
        envelope_args = args["envelope_args"]

        # 2. call Envelopes::create API method
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        if envelope_args.get("phone_number"):
            account_api = AccountsApi(api_client)
            (workflow_results, status, headers) = account_api.get_account_identity_verification_with_http_info(
                account_id=args["account_id"]
            )
            remaining = headers.get("X-RateLimit-Remaining")
            reset = headers.get("X-RateLimit-Reset")
        
            if remaining is not None and reset is not None:
                reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
                print(f"API calls remaining: {remaining}")
                print(f"Next Reset: {reset_date}")

            workflow_id = None
            if workflow_results.identity_verification:
                for workflow in workflow_results.identity_verification:
                    if workflow.default_name == "Phone Authentication":
                        workflow_id = workflow.workflow_id
                        break

            if workflow_id is None:
                raise ValueError("IDENTITY_WORKFLOW_INVALID_ID")

            envelope_args["workflow_id"] = workflow_id

        # Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args)

        envelope_api = EnvelopesApi(api_client)
        (results, status, headers) = envelope_api.create_envelope_with_http_info(account_id=args["account_id"], envelope_definition=envelope_definition)
        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        envelope_id = results.envelope_id
        #ds-snippet-end:eSign44Step3

        # 3. Create the Recipient View request object
        #ds-snippet-start:eSign44Step4
        recipient_view_request = RecipientViewRequest(
            authentication_method="none",
            client_user_id=envelope_args["signer_client_id"],
            recipient_id="1",
            return_url=envelope_args["ds_return_url"] + "?state=123",
            user_name=envelope_args["signer_name"],
            email=envelope_args["signer_email"],
            ping_frequency=600,
            ping_url=envelope_args["ds_ping_url"],
            frame_ancestors=["http://localhost:3000", "https://apps-d.docusign.com"],
            message_origins=["https://apps-d.docusign.com"]
        )
        #ds-snippet-end:eSign44Step4
        
        # 4. Obtain the recipient_view_url for the embedded signing
        # Exceptions will be caught by the calling function
        
        #ds-snippet-start:eSign44Step5
        (results, status, headers) = envelope_api.create_recipient_view_with_http_info(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request
        )
        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")

        if remaining is not None and reset is not None:
            reset_date = dt.fromtimestamp(int(reset), tz=timezone.utc)
            print(f"API calls remaining: {remaining}")
            print(f"Next Reset: {reset_date}")

        return {"envelope_id": envelope_id, "redirect_url": results.url}
        #ds-snippet-end:eSign44Step5

    @classmethod
    #ds-snippet-start:eSign44Step2
    def make_envelope(cls, args):
        """
        Creates envelope
        args -- parameters for the envelope:
        signer_email, signer_name, signer_client_id
        returns an envelope definition
        """

        # document 1 (pdf) has tag /sn1/
        #
        # The envelope has one recipient.
        # recipient 1 - signer
        with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Create the document model
        document = Document(  # create the DocuSign document object
            document_base64=base64_file_content,
            name="Example document",  # can be different from actual file name
            file_extension="pdf",  # many different document types are accepted
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
            client_user_id=args["signer_client_id"]
        )

        if args.get("phone_number"):
            signer.identity_verification = RecipientIdentityVerification(
                workflow_id=args["workflow_id"],
                steps=None,
                id_check_configuration_name="",
                input_options = [
                    RecipientIdentityInputOption(
                        name="phone_number_list",
                        value_type="PhoneNumberList",
                        phone_number_list=[
                            RecipientIdentityPhoneNumber(
                                country_code=args["country_code"],
                                number=args["phone_number"]
                            )
                        ]
                    )
                ]
            )

        # Next, create the top level envelope definition and populate it.
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document sent from the Python SDK",
            documents=[document],
            # The Recipients object wants arrays for each recipient type
            recipients=Recipients(signers=[signer]),
            status="sent"  # requests that the envelope be created and sent.
        )

        return envelope_definition
        #ds-snippet-end:eSign44Step2

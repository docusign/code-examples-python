import base64
from os import path

from docusign_esign import AccountsApi, EnvelopesApi, RecipientViewRequest, Document, Signer, EnvelopeDefinition, SignHere, Tabs, \
    Recipients
from docusign_esign.client.api_exception import ApiException
from flask import session, url_for, request

from ...consts import authentication_method, demo_docs_path, pattern, signer_client_id
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg041CFREmbeddedSigningController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        # 1. Parse request arguments
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        country_code = pattern.sub("", request.form.get("country_code"))
        phone_number = pattern.sub("", request.form.get("phone_number"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "phone_number": phone_number,
            "country_code": country_code,
            "signer_client_id": signer_client_id,
            "ds_return_url": url_for("ds.ds_return", _external=True),
            "workflow_id": session['workflow_id']
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
        envelope_definition = cls.make_envelope(envelope_args)

        # Call Envelopes::create API method
        # Exceptions will be caught by the calling function
        # Step 4 start
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id
        # Step 4 end

        # Create the Recipient View request object
        # Step 5 start
        recipient_view_request = RecipientViewRequest(
            authentication_method=authentication_method,
            client_user_id=envelope_args["signer_client_id"],
            recipient_id="1",
            return_url=envelope_args["ds_return_url"],
            user_name=envelope_args["signer_name"],
            email=envelope_args["signer_email"]
        )
        # Step 5 end
        # Obtain the recipient_view_url for the embedded signing
        # Exceptions will be caught by the calling function
        # Step 6 start
        results = envelope_api.create_recipient_view(
            account_id=args["account_id"],
            envelope_id=envelope_id,
            recipient_view_request=recipient_view_request
        )
        # Step 6 end

        return {"envelope_id": envelope_id, "redirect_url": results.url}

    # Step 3 start
    @classmethod
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
            identity_verification={ "workflowId": session['workflow_id'], "steps": "null", "inputOptions":[{"name":"phone_number_list","valueType":"PhoneNumberList","phoneNumberList":[{"countryCode":args["country_code"],"code":"1","number":args["phone_number"]}]}], "idCheckConfigurationName":""},
            # Setting the client_user_id marks the signer as embedded
            client_user_id=args["signer_client_id"]
        )

        # Create a sign_here tab (field on the document)
        sign_here = SignHere(
            # DocuSign SignHere field/tab
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="-30",
            anchor_x_offset="20"
        )

        # Add the tabs model (including the sign_here tab) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer.tabs = Tabs(sign_here_tabs=[sign_here])

        # Next, create the top level envelope definition and populate it.
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document sent from the Python SDK",
            documents=[document],
            # The Recipients object wants arrays for each recipient type
            recipients=Recipients(signers=[signer]),
            status="sent"  # requests that the envelope be created and sent.
        )

        return envelope_definition
    # Step 3 end

    # Step 2 start
    @staticmethod
    def get_workflow(args):
        """Retrieve the workflow id"""
        try:
            api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
            # Step 3 start
            workflow_details = AccountsApi(api_client)
            workflow_response = workflow_details.get_account_identity_verification(account_id=args["account_id"])

            # Check that idv authentication is enabled
            # Find the workflow ID corresponding to the name "Phone Authentication"
            if workflow_response.identity_verification:
                for workflow in workflow_response.identity_verification:
                    if workflow.default_name == "SMS for access & signatures":
                        session['workflow_id'] = workflow.workflow_id
            # Step 3 end
                return session['workflow_id']

            else:
                return None

        except ApiException as err:
            return process_error(err)

    # Step 2 end
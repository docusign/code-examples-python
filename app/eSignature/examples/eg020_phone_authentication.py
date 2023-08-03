import base64
from os import path

from docusign_esign import AccountsApi, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, RecipientIdentityInputOption, RecipientIdentityPhoneNumber
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app, session, request

from ...consts import demo_docs_path, pattern
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error


class Eg020PhoneAuthenticationController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than the characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        country_code = pattern.sub("", request.form.get("country_code"))
        phone_number = pattern.sub("", request.form.get("phone_number"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "phone_number": phone_number,
            "country_code": country_code,
            "status": "sent",
            "workflow_id": session['workflow_id']
        }
        args = {
            "account_id": session["ds_account_id"],  # represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # represnts your {ACCESS_TOKEN}
            "envelope_args": envelope_args
        }
        return args

    @staticmethod
    def worker(args):
        """
        1. Create an api client
        2. Create an envelope definition object
        """
        # Construct your API headers
        #ds-snippet-start:eSign20Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign20Step2

        # Construct your envelope
        #ds-snippet-start:eSign20Step4
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document set"
        )

        # Open the example file
        with open(path.join(demo_docs_path, DS_CONFIG["doc_pdf"]), "rb") as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode("ascii")

        # Add a document
        document1 = Document(  # create the DocuSign document object
            document_base64=base64_file_content,
            document_id="1",  # a label used to reference the doc
            file_extension="pdf",  # many different document types are accepted
            name="Lorem"  # can be different from actual file name
        )

        envelope_definition.documents = [document1]
        envelope_definition.status = args["envelope_args"]["status"]

        # Create your signature tab
        sign_here1 = SignHere(
            name="SignHereTab",
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20",
            tab_label="SignHereTab",
            page_number="1",
            document_id="1",
            # A 1- to 8-digit integer or 32-character GUID to match recipient IDs on your own systems.
            # This value is referenced in the Tabs element below to assign tabs on a per-recipient basis.
            recipient_id="1"  # represents your {RECIPIENT_ID}
        )

        signer1 = Signer(
            email=args["envelope_args"]["signer_email"],  # Represents your {signer_email}
            name=args["envelope_args"]["signer_name"],  # Represents your {signer_name}
            role_name="",
            note="",
            status="created",
            delivery_method="email",
            recipient_id="1",  # Represents your {RECIPIENT_ID}
            routing_order="1",
            identity_verification={ "workflowId": session['workflow_id'], "steps": "null", "inputOptions":[{"name":"phone_number_list","valueType":"PhoneNumberList","phoneNumberList":[{"countryCode":args["envelope_args"]["country_code"],"code":"1","number":args["envelope_args"]["phone_number"]}]}], "idCheckConfigurationName":""},
            tabs=Tabs(sign_here_tabs=[sign_here1])
        )

        # Tabs are set per recipient
        envelope_definition.recipients = Recipients(signers=[signer1])
        #ds-snippet-end:eSign20Step4
        
        # Call the eSignature REST API
        #ds-snippet-start:eSign20Step5
        envelopes_api = EnvelopesApi(api_client)
        results = envelopes_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
        #ds-snippet-end:eSign20Step5

        return results

    @staticmethod
    def get_workflow(args):
        """Retrieve the workflow id"""
        try:
            api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
            #ds-snippet-start:eSign20Step3
            workflow_details = AccountsApi(api_client)
            workflow_response = workflow_details.get_account_identity_verification(account_id=args["account_id"])

            # Check that idv authentication is enabled
            # Find the workflow ID corresponding to the name "Phone Authentication"
            if workflow_response.identity_verification:
                for workflow in workflow_response.identity_verification:
                    if workflow.default_name == "Phone Authentication":
                        session['workflow_id'] = workflow.workflow_id
            #ds-snippet-end:eSign20Step3
                return session['workflow_id']

            else:
                return None

        except ApiException as err:
            return process_error(err)
    

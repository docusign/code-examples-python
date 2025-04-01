import base64
import requests
from os import path

from docusign_esign import EnvelopesApi, Text, Document, Signer, EnvelopeDefinition, SignHere, Tabs, \
    Recipients
from flask import session, request

from ...consts import demo_docs_path, pattern
from ...docusign import create_api_client
from ...ds_config import DS_CONFIG


class Eg001SetConnectedFieldsController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        # Parse request arguments
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        selected_app_id = pattern.sub("", request.form.get("app_id"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
        }
        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "selected_app_id": selected_app_id,
            "envelope_args": envelope_args
        }
        return args
    
    @staticmethod
    def get_tab_groups(args):
        """
        1. Get the list of tab groups
        2. Filter by action contract and tab label
        3. Create a list of unique apps
        """

        #ds-snippet-start:ConnectedFields1Step2
        headers = {
            "Authorization": "Bearer " + args['access_token'],
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        #ds-snippet-end:ConnectedFields1Step2

        #ds-snippet-start:ConnectedFields1Step3
        url = f"{args['base_path']}/v1/accounts/{args['account_id']}/connected-fields/tab-groups"
        
        response = requests.get(url, headers=headers)
        response_data = response.json()

        filtered_apps = list(
            app for app in response_data
            if any(
                ("extensionData" in tab and "actionContract" in tab["extensionData"] and "Verify" in tab["extensionData"]["actionContract"]) or
                ("tabLabel" in tab and "connecteddata" in tab["tabLabel"])
                for tab in app.get("tabs", [])
            )
        )

        unique_apps = list({app['appId']: app for app in filtered_apps}.values())
        #ds-snippet-end:ConnectedFields1Step3

        return unique_apps
    
    @staticmethod
    #ds-snippet-start:ConnectedFields1Step4
    def extract_verification_data(selected_app_id, tab):
        extension_data = tab["extensionData"]

        return {
            "app_id": selected_app_id,
            "extension_group_id": extension_data["extensionGroupId"] if "extensionGroupId" in extension_data else "",
            "publisher_name": extension_data["publisherName"] if "publisherName" in extension_data else "",
            "application_name": extension_data["applicationName"] if "applicationName" in extension_data else "",
            "action_name": extension_data["actionName"] if "actionName" in extension_data else "",
            "action_input_key": extension_data["actionInputKey"] if "actionInputKey" in extension_data else "",
            "action_contract": extension_data["actionContract"] if "actionContract" in extension_data else "",
            "extension_name": extension_data["extensionName"] if "extensionName" in extension_data else "",
            "extension_contract": extension_data["extensionContract"] if "extensionContract" in extension_data else "",
            "required_for_extension": extension_data["requiredForExtension"] if "requiredForExtension" in extension_data else "",
            "tab_label": tab["tabLabel"],
            "connection_key": (
                extension_data["connectionInstances"][0]["connectionKey"]
                if "connectionInstances" in extension_data and extension_data["connectionInstances"]
                else ""
            ),
            "connection_value": (
                extension_data["connectionInstances"][0]["connectionValue"]
                if "connectionInstances" in extension_data and extension_data["connectionInstances"]
                else ""
            ),
        }
    #ds-snippet-end:ConnectedFields1Step4

    @classmethod
    def send_envelope(cls, args, app):
        """
        1. Create the envelope request object
        2. Send the envelope
        3. Obtain the envelope_id
        """
        #ds-snippet-start:ConnectedFields1Step6
        envelope_args = args["envelope_args"]
        # Create the envelope request object
        envelope_definition = cls.make_envelope(envelope_args, app)

        # Call Envelopes::create API method
        # Exceptions will be caught by the calling function
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        envelope_id = results.envelope_id
        #ds-snippet-end:ConnectedFields1Step6

        return {"envelope_id": envelope_id}

    @classmethod
    #ds-snippet-start:ConnectedFields1Step5
    def make_envelope(cls, args, app):
        """
        Creates envelope
        args -- parameters for the envelope:
        signer_email, signer_name
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
            routing_order="1"
        )

        # Create a sign_here tab (field on the document)
        sign_here = SignHere(
            anchor_string="/sn1/",
            anchor_units="pixels",
            anchor_y_offset="10",
            anchor_x_offset="20"
        )

        # Create text tabs (field on the document)
        text_tabs = []
        for tab in (t for t in app["tabs"] if "SuggestionInput" not in t["tabLabel"]):
            verification_data = cls.extract_verification_data(app["appId"], tab)
            extension_data = cls.get_extension_data(verification_data)

            text_tab = {
                "requireInitialOnSharedChange": False,
                "requireAll": False,
                "name": verification_data["application_name"],
                "required": True,
                "locked": False,
                "disableAutoSize": False,
                "maxLength": 4000,
                "tabLabel": verification_data["tab_label"],
                "font": "lucidaconsole",
                "fontColor": "black",
                "fontSize": "size9",
                "documentId": "1",
                "recipientId": "1",
                "pageNumber": "1",
                "xPosition": f"{70 + 100 * int(len(text_tabs) / 10)}",
                "yPosition": f"{560 + 20 * (len(text_tabs) % 10)}",
                "width": "84",
                "height": "22",
                "templateRequired": False,
                "tabType": "text",
                "tooltip": verification_data["action_input_key"],
                "extensionData": extension_data
            }
            text_tabs.append(text_tab)

        # Add the tabs model (including the sign_here and text tabs) to the signer
        # The Tabs object wants arrays of the different field/tab types
        signer.tabs = Tabs(sign_here_tabs=[sign_here], text_tabs=text_tabs)

        # Next, create the top level envelope definition and populate it.
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document",
            documents=[document],
            # The Recipients object wants arrays for each recipient type
            recipients=Recipients(signers=[signer]),
            status="sent"  # requests that the envelope be created and sent.
        )

        return envelope_definition
    
    def get_extension_data(verification_data):
        return {
            "extensionGroupId": verification_data["extension_group_id"],
            "publisherName": verification_data["publisher_name"],
            "applicationId": verification_data["app_id"],
            "applicationName": verification_data["application_name"],
            "actionName": verification_data["action_name"],
            "actionContract": verification_data["action_contract"],
            "extensionName": verification_data["extension_name"],
            "extensionContract": verification_data["extension_contract"],
            "requiredForExtension": verification_data["required_for_extension"],
            "actionInputKey": verification_data["action_input_key"],
            "extensionPolicy": 'MustVerifyToSign',
            "connectionInstances": [
                {
                    "connectionKey": verification_data["connection_key"],
                    "connectionValue": verification_data["connection_value"],
                }
            ]
        }
    #ds-snippet-end:ConnectedFields1Step5

import uuid
from docusign_maestro import ApiClient, WorkflowManagementApi, WorkflowDefinition, DeployRequest, \
    DSWorkflowTrigger, DSWorkflowVariableFromVariable, DeployStatus

import json


def create_maestro_api_client(base_path, access_token):
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {access_token}")

    return api_client


def create_workflow(args):
    signer_id = str(uuid.uuid4())
    cc_id = str(uuid.uuid4())
    trigger_id = "wfTrigger"

    participants = {
        signer_id: {
            "participantRole": "Signer"
        },
        cc_id: {
            "participantRole": "CC"
        }
    }

    dac_id_field = f"dacId_{trigger_id}"
    id_field = f"id_{trigger_id}"
    signer_name_field = f"signerName_{trigger_id}"
    signer_email_field = f"signerEmail_{trigger_id}"
    cc_name_field = f"ccName_{trigger_id}"
    cc_email_field = f"ccEmail_{trigger_id}"

    trigger = DSWorkflowTrigger(
        name="Get_URL",
        type="Http",
        http_type="Get",
        id=trigger_id,
        input={
            'metadata': {
                'customAttributes': {}
            },
            'payload': {
                dac_id_field: {
                    'source': 'step',
                    'propertyName': 'dacId',
                    'stepId': trigger_id
                },
                id_field: {
                    'source': 'step',
                    'propertyName': 'id',
                    'stepId': trigger_id
                },
                signer_name_field: {
                    'source': 'step',
                    'propertyName': 'signerName',
                    'stepId': trigger_id
                },
                signer_email_field: {
                    'source': 'step',
                    'propertyName': 'signerEmail',
                    'stepId': trigger_id
                },
                cc_name_field: {
                    'source': 'step',
                    'propertyName': 'ccName',
                    'stepId': trigger_id
                },
                cc_email_field: {
                    'source': 'step',
                    'propertyName': 'ccEmail',
                    'stepId': trigger_id
                }
            },
            'participants': {}
        },
        output={
            dac_id_field: {
                'source': 'step',
                'propertyName': 'dacId',
                'stepId': trigger_id
            }
        }
    )

    variables = {
        dac_id_field: DSWorkflowVariableFromVariable(source='step', property_name='dacId', step_id=trigger_id),
        id_field: DSWorkflowVariableFromVariable(source='step', property_name='id', step_id=trigger_id),
        signer_name_field: DSWorkflowVariableFromVariable(source='step', property_name='signerName',
                                                          step_id=trigger_id),
        signer_email_field: DSWorkflowVariableFromVariable(source='step', property_name='signerEmail',
                                                           step_id=trigger_id),
        cc_name_field: DSWorkflowVariableFromVariable(source='step', property_name='ccName', step_id=trigger_id),
        cc_email_field: DSWorkflowVariableFromVariable(source='step', property_name='ccEmail', step_id=trigger_id),
        'envelopeId_step2': DSWorkflowVariableFromVariable(source='step', property_name='envelopeId', step_id='step2',
                                                           type='String'),
        'combinedDocumentsBase64_step2': DSWorkflowVariableFromVariable(source='step',
                                                                        property_name='combinedDocumentsBase64',
                                                                        step_id='step2', type='File'),
        'fields.signer.text.value_step2': DSWorkflowVariableFromVariable(source='step',
                                                                         property_name='fields.signer.text.value',
                                                                         step_id='step2', type='String')
    }

    step1 = {
        'id': 'step1',
        'name': 'Set Up Invite',
        'moduleName': 'Notification-SendEmail',
        'configurationProgress': 'Completed',
        'type': 'DS-EmailNotification',
        'config': {
            'templateType': 'WorkflowParticipantNotification',
            'templateVersion': 1,
            'language': 'en',
            'sender_name': 'DocuSign Orchestration',
            'sender_alias': 'Orchestration',
            'participantId': signer_id
        },
        'input': {
            'recipients': [
                {
                    'name': {
                        'source': 'step',
                        'propertyName': 'signerName',
                        'stepId': trigger_id
                    },
                    'email': {
                        'source': 'step',
                        'propertyName': 'signerEmail',
                        'stepId': trigger_id
                    }
                }
            ],
            'mergeValues': {
                'CustomMessage': 'Follow this link to access and complete the workflow.',
                'ParticipantFullName': {
                    'source': 'step',
                    'propertyName': 'signerName',
                    'stepId': trigger_id
                }
            }
        },
        'output': {}
    }

    step2 = {
        "id": 'step2',
        "name": 'Get Signatures',
        "moduleName": 'ESign',
        "configurationProgress": 'Completed',
        "type": 'DS-Sign',
        "config": {
            "participantId": signer_id,
        },
        "input": {
            "isEmbeddedSign": True,
            "documents": [
                {
                    "type": 'FromDSTemplate',
                    "eSignTemplateId": args["template_id"],
                },
            ],
            "emailSubject": 'Please sign this document',
            "emailBlurb": '',
            "recipients": {
                "signers": [
                    {
                        "defaultRecipient": 'false',
                        "tabs": {
                            "signHereTabs": [
                                {
                                    "stampType": 'signature',
                                    "name": 'SignHere',
                                    "tabLabel": 'Sign Here',
                                    "scaleValue": '1',
                                    "optional": 'false',
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '191',
                                    "yPosition": '148',
                                    "tabId": '1',
                                    "tabType": 'signhere',
                                },
                            ],
                            'textTabs': [
                                {
                                    "requireAll": 'false',
                                    "value": '',
                                    "required": 'false',
                                    "locked": 'false',
                                    "concealValueOnDocument": 'false',
                                    "disableAutoSize": 'false',
                                    "tabLabel": 'text',
                                    "font": 'helvetica',
                                    "fontSize": 'size14',
                                    "localePolicy": {},
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '153',
                                    "yPosition": '230',
                                    "width": '84',
                                    "height": '23',
                                    "tabId": '2',
                                    "tabType": 'text',
                                },
                            ],
                            "checkboxTabs": [
                                {
                                    "name": '',
                                    "tabLabel": 'ckAuthorization',
                                    "selected": 'false',
                                    "selectedOriginal": 'false',
                                    "requireInitialOnSharedChange": 'false',
                                    "required": 'true',
                                    "locked": 'false',
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '75',
                                    "yPosition": '417',
                                    "width": '0',
                                    "height": '0',
                                    "tabId": '3',
                                    "tabType": 'checkbox',
                                },
                                {
                                    "name": '',
                                    "tabLabel": 'ckAuthentication',
                                    "selected": 'false',
                                    "selectedOriginal": 'false',
                                    "requireInitialOnSharedChange": 'false',
                                    "required": 'true',
                                    "locked": 'false',
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '75',
                                    "yPosition": '447',
                                    "width": '0',
                                    "height": '0',
                                    "tabId": '4',
                                    "tabType": 'checkbox',
                                },
                                {
                                    "name": '',
                                    "tabLabel": 'ckAgreement',
                                    "selected": 'false',
                                    "selectedOriginal": 'false',
                                    "requireInitialOnSharedChange": 'false',
                                    "required": 'true',
                                    "locked": 'false',
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '75',
                                    "yPosition": '478',
                                    "width": '0',
                                    "height": '0',
                                    "tabId": '5',
                                    "tabType": 'checkbox',
                                },
                                {
                                    "name": '',
                                    "tabLabel": 'ckAcknowledgement',
                                    "selected": 'false',
                                    "selectedOriginal": 'false',
                                    "requireInitialOnSharedChange": 'false',
                                    "required": 'true',
                                    "locked": 'false',
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '75',
                                    "yPosition": '508',
                                    "width": '0',
                                    "height": '0',
                                    "tabId": '6',
                                    "tabType": 'checkbox',
                                },
                            ],
                            "radioGroupTabs": [
                                {
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "groupName": 'radio1',
                                    "radios": [
                                        {
                                            "pageNumber": '1',
                                            "xPosition": '142',
                                            "yPosition": '384',
                                            "value": 'white',
                                            "selected": 'false',
                                            "tabId": '7',
                                            "required": 'false',
                                            "locked": 'false',
                                            "bold": 'false',
                                            "italic": 'false',
                                            "underline": 'false',
                                            "fontColor": 'black',
                                            "fontSize": 'size7',
                                        },
                                        {
                                            "pageNumber": '1',
                                            "xPosition": '74',
                                            "yPosition": '384',
                                            "value": 'red',
                                            "selected": 'false',
                                            "tabId": '8',
                                            "required": 'false',
                                            "locked": 'false',
                                            "bold": 'false',
                                            "italic": 'false',
                                            "underline": 'false',
                                            "fontColor": 'black',
                                            "fontSize": 'size7',
                                        },
                                        {
                                            "pageNumber": '1',
                                            "xPosition": '220',
                                            "yPosition": '384',
                                            "value": 'blue',
                                            "selected": 'false',
                                            "tabId": '9',
                                            "required": 'false',
                                            "locked": 'false',
                                            "bold": 'false',
                                            "italic": 'false',
                                            "underline": 'false',
                                            "fontColor": 'black',
                                            "fontSize": 'size7',
                                        },
                                    ],
                                    "shared": 'false',
                                    "requireInitialOnSharedChange": 'false',
                                    "requireAll": 'false',
                                    "tabType": 'radiogroup',
                                    "value": '',
                                    "originalValue": '',
                                },
                            ],
                            "listTabs": [
                                {
                                    "listItems": [
                                        {
                                            "text": 'Red',
                                            "value": 'red',
                                            "selected": 'false',
                                        },
                                        {
                                            "text": 'Orange',
                                            "value": 'orange',
                                            "selected": 'false',
                                        },
                                        {
                                            "text": 'Yellow',
                                            "value": 'yellow',
                                            "selected": 'false',
                                        },
                                        {
                                            "text": 'Green',
                                            "value": 'green',
                                            "selected": 'false',
                                        },
                                        {
                                            "text": 'Blue',
                                            "value": 'blue',
                                            "selected": 'false',
                                        },
                                        {
                                            "text": 'Indigo',
                                            "value": 'indigo',
                                            "selected": 'false',
                                        },
                                        {
                                            "text": 'Violet',
                                            "value": 'violet',
                                            "selected": 'false',
                                        },
                                    ],
                                    "value": '',
                                    "originalValue": '',
                                    "required": 'false',
                                    "locked": 'false',
                                    "requireAll": 'false',
                                    "tabLabel": 'list',
                                    "font": 'helvetica',
                                    "fontSize": 'size14',
                                    "localePolicy": {},
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '142',
                                    "yPosition": '291',
                                    "width": '78',
                                    "height": '0',
                                    "tabId": '10',
                                    "tabType": 'list',
                                },
                            ],
                            "numericalTabs": [
                                {
                                    "validationType": 'currency',
                                    "value": '',
                                    "required": 'false',
                                    "locked": 'false',
                                    "concealValueOnDocument": 'false',
                                    "disableAutoSize": 'false',
                                    "tabLabel": 'numericalCurrency',
                                    "font": 'helvetica',
                                    "fontSize": 'size14',
                                    "localePolicy": {
                                        "cultureName": 'en-US',
                                        "currencyPositiveFormat":
                                            'csym_1_comma_234_comma_567_period_89',
                                        "currencyNegativeFormat":
                                            'opar_csym_1_comma_234_comma_567_period_89_cpar',
                                        "currencyCode": 'usd',
                                    },
                                    "documentId": '1',
                                    "recipientId": '1',
                                    "pageNumber": '1',
                                    "xPosition": '163',
                                    "yPosition": '260',
                                    "width": '84',
                                    "height": '0',
                                    "tabId": '11',
                                    "tabType": 'numerical',
                                },
                            ],
                        },
                        "signInEachLocation": 'false',
                        "agentCanEditEmail": 'false',
                        "agentCanEditName": 'false',
                        "requireUploadSignature": 'false',
                        "name": {
                            "source": 'step',
                            "propertyName": 'signerName',
                            "stepId": trigger_id,
                        },
                        "email": {
                            "source": 'step',
                            "propertyName": 'signerEmail',
                            "stepId": trigger_id,
                        },
                        "recipientId": '1',
                        "recipientIdGuid": '00000000-0000-0000-0000-000000000000',
                        "accessCode": '',
                        "requireIdLookup": 'false',
                        "routingOrder": '1',
                        "note": '',
                        "roleName": 'signer',
                        "completedCount": '0',
                        "deliveryMethod": 'email',
                        "templateLocked": 'false',
                        "templateRequired": 'false',
                        "inheritEmailNotificationConfiguration": 'false',
                        "recipientType": 'signer',
                    },
                ],
                "carbonCopies": [
                    {
                        "agentCanEditEmail": 'false',
                        "agentCanEditName": 'false',
                        "name": {
                            "source": 'step',
                            "propertyName": 'ccName',
                            "stepId": trigger_id,
                        },
                        "email": {
                            "source": 'step',
                            "propertyName": 'ccEmail',
                            "stepId": trigger_id,
                        },
                        "recipientId": '2',
                        "recipientIdGuid": '00000000-0000-0000-0000-000000000000',
                        "accessCode": '',
                        "requireIdLookup": 'false',
                        "routingOrder": '2',
                        "note": '',
                        "roleName": 'cc',
                        "completedCount": '0',
                        "deliveryMethod": 'email',
                        "templateLocked": 'false',
                        "templateRequired": 'false',
                        "inheritEmailNotificationConfiguration": 'false',
                        "recipientType": 'carboncopy',
                    },
                ],
                "certifiedDeliveries": [],
            },
        },
        "output": {
            "envelopeId_step2": {
                "source": 'step',
                "propertyName": 'envelopeId',
                "stepId": 'step2',
                "type": 'String',
            },
            "combinedDocumentsBase64_step2": {
                "source": 'step',
                "propertyName": 'combinedDocumentsBase64',
                "stepId": 'step2',
                "type": 'File',
            },
            'fields.signer.text.value_step2': {
                "source": 'step',
                "propertyName": 'fields.signer.text.value',
                "stepId": 'step2',
                "type": 'String',
            },
        },
    }

    step3 = {
        "id": 'step3',
        "name": 'Show a Confirmation Screen',
        "moduleName": 'ShowConfirmationScreen',
        "configurationProgress": 'Completed',
        "type": 'DS-ShowScreenStep',
        "config": {
            "participantId": signer_id
        },
        "input": {
            "httpType": "Post",
            "payload": {
                "participantId": signer_id,
                "confirmationMessage": {
                    "title": 'Tasks complete',
                    "description": 'You have completed all your workflow tasks.'
                }
            }
        },
        "output": {}
    }

    workflow_definition = WorkflowDefinition(
        workflow_name="Example workflow - send invite to signer",
        workflow_description="",
        document_version="1.0.0",
        schema_version="1.0.0",
        account_id=args["account_id"],
        participants=participants,
        trigger=trigger,
        variables=variables,
        steps=[step1, step2, step3]
    )

    api_client = create_maestro_api_client(args["base_path"], args["access_token"])
    workflow_management_api = WorkflowManagementApi(api_client)
    # body = {"workflowDefinition": workflow_definition.__dict__}
    workflow = workflow_management_api.create_workflow_definition(
        args["account_id"],
        {"workflowDefinition": workflow_definition}
    )

    return workflow.workflow_definition_id


def publish_workflow(args, workflow_id):
    api_client = create_maestro_api_client(args["base_path"], args["access_token"])
    workflow_management_api = WorkflowManagementApi(api_client)

    try:
        deploy_request = DeployRequest(
            deployment_status=DeployStatus.PUBLISH
        )
        workflow_management_api.publish_or_un_publish_workflow_definition(
            args["account_id"],
            workflow_id,
            deploy_request
        )
    except Exception as err:
        if hasattr(err, 'response') and hasattr(err.response, 'data'):
            response_data = json.loads(err.response.data)
            if 'message' in response_data:
                is_consent_required = response_data['message'] == 'Consent required'
                if is_consent_required:
                    return response_data["consentUrl"]
        raise err

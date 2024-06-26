from docusign_maestro import WorkflowManagementApi, WorkflowTriggerApi, TriggerPayload
from flask import session, request

from app.docusign.utils import get_parameter_value_from_url
from app.ds_config import DS_CONFIG
from app.maestro.utils import create_maestro_api_client
from app.consts import pattern


class Eg001TriggerWorkflowController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        return {
            "account_id": session["ds_account_id"],
            "base_path": DS_CONFIG["maestro_api_client_host"],
            "access_token": session["ds_access_token"],
            "workflow_id": session["workflow_id"],
            "instance_name": pattern.sub("", request.form.get("instance_name")),
            "signer_email": pattern.sub("", request.form.get("signer_email")),
            "signer_name": pattern.sub("", request.form.get("signer_name")),
            "cc_email": pattern.sub("", request.form.get("cc_email")),
            "cc_name": pattern.sub("", request.form.get("cc_name")),
        }
    
    @staticmethod
    def get_workflow_definitions(args):
        api_client = create_maestro_api_client(args["base_path"], args["access_token"])
        workflow_management_api = WorkflowManagementApi(api_client)
        workflow_definitions = workflow_management_api.get_workflow_definitions(args["account_id"], status="active")

        return workflow_definitions
    
    @staticmethod
    def get_workflow_definition(args):
        #ds-snippet-start:Maestro1Step2
        api_client = create_maestro_api_client(args["base_path"], args["access_token"])
        #ds-snippet-end:Maestro1Step2

        #ds-snippet-start:Maestro1Step3
        workflow_management_api = WorkflowManagementApi(api_client)
        workflow_definition = workflow_management_api.get_workflow_definition(args["account_id"], args["workflow_id"])
        #ds-snippet-end:Maestro1Step3

        return workflow_definition

    @staticmethod
    def trigger_workflow(workflow, args):
        api_client = create_maestro_api_client(args["base_path"], args["access_token"])

        #ds-snippet-start:Maestro1Step4
        trigger_payload = TriggerPayload(
            instance_name=args["instance_name"],
            participant={},
            payload={
                "signerEmail": args["signer_email"],
                "signerName": args["signer_name"],
                "ccEmail": args["cc_email"],
                "ccName": args["cc_name"]
            },
            metadata={}
        )
        mtid = get_parameter_value_from_url(workflow.trigger_url, "mtid")
        mtsec = get_parameter_value_from_url(workflow.trigger_url, "mtsec")
        #ds-snippet-end:Maestro1Step4

        #ds-snippet-start:Maestro1Step5
        workflow_trigger_api = WorkflowTriggerApi(api_client)
        trigger_response = workflow_trigger_api.trigger_workflow(
            args["account_id"],
            args["workflow_id"],
            trigger_payload,
            mtid=mtid, mtsec=mtsec
        )
        #ds-snippet-end:Maestro1Step5
        return trigger_response

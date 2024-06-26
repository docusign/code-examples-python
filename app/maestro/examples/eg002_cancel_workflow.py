from docusign_maestro import WorkflowInstanceManagementApi
from flask import session

from app.ds_config import DS_CONFIG
from app.maestro.utils import create_maestro_api_client


class Eg002CancelWorkflowController:
    @staticmethod
    def get_args():
        """Get request and session arguments"""
        return {
            "account_id": session["ds_account_id"],
            "base_path": DS_CONFIG["maestro_api_client_host"],
            "access_token": session["ds_access_token"],
            "workflow_id": session["workflow_id"],
            "instance_id": session["instance_id"]
        }
    
    @staticmethod
    def get_instance_state(args):
        api_client = create_maestro_api_client(args["base_path"], args["access_token"])
        workflow_instance_management_api = WorkflowInstanceManagementApi(api_client)
        instance = workflow_instance_management_api.get_workflow_instance(
            args["account_id"],
            args["workflow_id"],
            args["instance_id"]
        )

        return instance.instance_state
    
    @staticmethod
    def cancel_workflow_instance(args):
        #ds-snippet-start:Maestro2Step2
        api_client = create_maestro_api_client(args["base_path"], args["access_token"])
        #ds-snippet-end:Maestro2Step2

        #ds-snippet-start:Maestro2Step3
        workflow_instance_management_api = WorkflowInstanceManagementApi(api_client)
        cancel_result = workflow_instance_management_api.cancel_workflow_instance(
            args["account_id"],
            args["instance_id"]
        )
        #ds-snippet-end:Maestro2Step3
        return cancel_result

"""Example 001: How to trigger a Maestro workflow"""

import json

from docusign_maestro.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ..examples.eg001_trigger_workflow import Eg001TriggerWorkflowController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE
from ..utils import create_workflow, publish_workflow

example_number = 1
api = API_TYPE["MAESTRO"]
eg = f"mseg00{example_number}"  # reference (and url) for this example
mseg001 = Blueprint(eg, __name__)


@mseg001.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def trigger_workflow():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show results
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg001TriggerWorkflowController.get_args()
    try:
        # 1. Call the worker method
        print("args:\n\n")
        print(args)
        workflow = Eg001TriggerWorkflowController.get_workflow_definition(args)
        results = Eg001TriggerWorkflowController.trigger_workflow(workflow, args)
        session["instance_id"] = results.instance_id
    except ApiException as err:
        if hasattr(err, "status"):
            if err.status == 403:
                return render_template(
                    "error.html",
                    err=err,
                    error_code=err.status,
                    error_message=session["manifest"]["SupportingTexts"]["ContactSupportToEnableFeature"]
                                  .format("Maestro")
                )

        return process_error(err)
    # 3. Show results
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"],
        json=json.dumps(json.dumps(results.to_dict()))
    )


@mseg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)
    additional_page_data = next((p for p in example["AdditionalPage"] if p["Name"] == "publish_workflow"), None)

    args = {
        "account_id": session["ds_account_id"],
        "base_path": DS_CONFIG["maestro_api_client_host"],
        "access_token": session["ds_access_token"],
        "template_id": session.get("template_id", None)
    }
    try:
        workflows = Eg001TriggerWorkflowController.get_workflow_definitions(args)

        if workflows.count > 0:
            sorted_workflows = sorted(
                workflows.value,
                key=lambda w: w.last_updated_date,
                reverse=True
            )

            if sorted_workflows:
                session["workflow_id"] = sorted_workflows[0].id

        if "workflow_id" not in session:
            if "template_id" not in session:
                return render_template(
                    "maestro/eg001_trigger_workflow.html",
                    title=example["ExampleName"],
                    example=example,
                    template_ok=False,
                    source_file="eg001_trigger_workflow.py",
                    source_url=DS_CONFIG["github_example_url"] + "eg001_trigger_workflow.py",
                    documentation=DS_CONFIG["documentation"] + eg,
                    show_doc=DS_CONFIG["documentation"],
                )

            # if there is no workflow, then create one
            session["workflow_id"] = create_workflow(args)
            consent_url = publish_workflow(args, session["workflow_id"]) 

            if consent_url:
                return render_template(
                    "maestro/eg001_publish_workflow.html",
                    title=example["ExampleName"],
                    message=additional_page_data["ResultsPageText"],
                    consent_url=consent_url
                )

    except ApiException as err:
        if hasattr(err, "status"):
            if err.status == 403:
                return render_template(
                    "error.html",
                    err=err,
                    error_code=err.status,
                    error_message=session["manifest"]["SupportingTexts"]["ContactSupportToEnableFeature"]
                                  .format("Maestro")
                )

        return process_error(err)

    return render_template(
        "maestro/eg001_trigger_workflow.html",
        title=example["ExampleName"],
        example=example,
        template_ok=True,
        source_file="eg001_trigger_workflow.py",
        source_url=DS_CONFIG["github_example_url"] + "eg001_trigger_workflow.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

@mseg001.route(f"/{eg}publish", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def publish_workflow_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)
    additional_page_data = next((p for p in example["AdditionalPage"] if p["Name"] == "publish_workflow"), None)

    args = {
        "account_id": session["ds_account_id"],
        "base_path": DS_CONFIG["maestro_api_client_host"],
        "access_token": session["ds_access_token"]
    }
    try:
        consent_url = publish_workflow(args, session["workflow_id"])

        if consent_url:
            return render_template(
                "maestro/eg001_publish_workflow.html",
                title=example["ExampleName"],
                message=additional_page_data["ResultsPageText"],
                consent_url=consent_url
            )

    except ApiException as err:
        if hasattr(err, "status"):
            if err.status == 403:
                return render_template(
                    "error.html",
                    err=err,
                    error_code=err.status,
                    error_message=session["manifest"]["SupportingTexts"]["ContactSupportToEnableFeature"]
                                  .format("Maestro")
                )

        return process_error(err)

    return render_template(
        "maestro/eg001_trigger_workflow.html",
        title=example["ExampleName"],
        example=example,
        template_ok=True,
        source_file="eg001_trigger_workflow.py",
        source_url=DS_CONFIG["github_example_url"] + "eg001_trigger_workflow.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

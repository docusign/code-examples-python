"""Example 002: How to cancel a Maestro workflow instance"""

import json

from docusign_maestro.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ..examples.eg002_cancel_workflow import Eg002CancelWorkflowController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 2
api = API_TYPE["MAESTRO"]
eg = f"mseg00{example_number}"  # reference (and url) for this example
mseg002 = Blueprint(eg, __name__)


@mseg002.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def cancel_workflow():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show results
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg002CancelWorkflowController.get_args()
    try:
        # 1. Call the worker method
        results = Eg002CancelWorkflowController.cancel_workflow_instance(args)
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
        message=example["ResultsPageText"].format(session["instance_id"]),
        json=json.dumps(json.dumps(results.to_dict()))
    )


@mseg002.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    instance_ok = False
    workflow_id = session.get("workflow_id", None)
    instance_id = session.get("instance_id", None)
    if workflow_id and instance_id:
        args = {
            "account_id": session["ds_account_id"],
            "base_path": DS_CONFIG["maestro_api_client_host"],
            "access_token": session["ds_access_token"],
            "workflow_id": workflow_id,
            "instance_id": instance_id
        }

        try:
            state = Eg002CancelWorkflowController.get_instance_state(args)
            instance_ok = state.lower() == "in progress"
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
        "maestro/eg002_cancel_workflow.html",
        title=example["ExampleName"],
        example=example,
        instance_ok=instance_ok,
        workflow_id=workflow_id,
        instance_id=instance_id,
        source_file="eg002_cancel_workflow.py",
        source_url=DS_CONFIG["github_example_url"] + "eg002_cancel_workflow.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

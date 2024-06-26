"""Example 003: How to get the status of a Maestro workflow instance"""

import json

from docusign_maestro.client.api_exception import ApiException
from flask import render_template, Blueprint, session

from ..examples.eg003_get_workflow_status import Eg003GetWorkflowStatusController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 3
api = API_TYPE["MAESTRO"]
eg = f"mseg00{example_number}"  # reference (and url) for this example
mseg003 = Blueprint(eg, __name__)


@mseg003.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_workflow_status():
    """
    1. Get required arguments
    2. Call the worker method
    3. Show results
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg003GetWorkflowStatusController.get_args()
    try:
        # 1. Call the worker method
        results = Eg003GetWorkflowStatusController.get_workflow_instance(args)
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
        message=example["ResultsPageText"].format(results.instance_state),
        json=json.dumps(json.dumps(results.to_dict(), default=str))
    )


@mseg003.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    workflow_id = session.get("workflow_id", None)
    instance_id = session.get("instance_id", None)
    return render_template(
        "maestro/eg003_get_workflow_status.html",
        title=example["ExampleName"],
        example=example,
        workflow_id=workflow_id,
        instance_id=instance_id,
        source_file="eg003_get_workflow_status.py",
        source_url=DS_CONFIG["github_example_url"] + "eg003_get_workflow_status.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

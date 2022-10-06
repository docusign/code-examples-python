""" Example 032: Creating an envelope where the workflow is paused before the
envelope is sent to a second recipient """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg032_pause_signature_workflow import Eg032PauseSignatureWorkflowController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

example_number = 32
eg = f"eg0{example_number}"  # Reference (and URL) for this example
eg032 = Blueprint(eg, __name__)


@eg032.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["esign_manifest_url"])
@authenticate(eg=eg)
def pause_signature_workflow():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg032PauseSignatureWorkflowController.get_args()
    try:
        # 1. Call the worker method
        results = Eg032PauseSignatureWorkflowController.worker(args)
    except ApiException as err:
        return process_error(err)

    session["paused_envelope_id"] = results["paused_envelope_id"]  # Save for use by other examples which need an envelopeId

    # 2. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=f"The envelope has been created and sent!"
                f"<br/>Envelope ID {results['paused_envelope_id']}.<br/>"
                f"<p>To resume a workflow after the first recipient signs "
                f"the envelope use <a href='eg033'>example 33.</a><br/>"
    )


@eg032.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["esign_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    return render_template(
        "eg032_pause_signature_workflow.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg032_pause_signature_workflow.py",
        source_url=DS_CONFIG["github_example_url"] + "eg032_pause_signature_workflow.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer1_name=DS_CONFIG["signer_name"],
        signer1_email=DS_CONFIG["signer_email"]
    )

""" Example 033: Resuming an envelope workflow that has been paused """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg033_unpause_signature_workflow import Eg033UnpauseSignatureWorkflowController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...docusign.utils import is_cfr
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 33
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # Reference (and URL) for this example
eg033 = Blueprint(eg, __name__)


@eg033.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def unpause_signature_workflow():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg033UnpauseSignatureWorkflowController.get_args()
    try:
        # 1. Call the worker method
        results = Eg033UnpauseSignatureWorkflowController.worker(args)
    except ApiException as err:
        return process_error(err)

    # 2. Render success response with envelopeId
    return render_template(
        "example_done.html",
        envelope_ok=True,
        title=example["ExampleName"],
        message=f"The envelope workflow has been resumed and the envelope "
                f"has been sent to a second recipient!<br/>"
                f"Envelope ID {results['envelope_id']}."
    )


@eg033.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    cfr_status = is_cfr(session["ds_access_token"], session["ds_account_id"], session["ds_base_path"])
    if cfr_status == "enabled":
        if DS_CONFIG["quickstart"] == "true":
            return redirect(url_for("eg041.get_view"))
        else:
            return render_template("cfr_error.html", title="Error")

    return render_template(
        "eSignature/eg033_unpause_signature_workflow.html",
        title=example["ExampleName"],
        example=example,
        envelope_ok="paused_envelope_id" in session,
        source_file= "eg033_unpause_signature_workflow.py",
        source_url=DS_CONFIG["github_example_url"] + "eg033_unpause_signature_workflow.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

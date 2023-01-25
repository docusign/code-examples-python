""" Example 023: ID Verificiation Based authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint, session

from ..examples.eg023_idv_authentication import Eg023IDVAuthenticationController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 23
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # Reference (and URL) for this example
eg023 = Blueprint(eg, __name__)


@eg023.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def idv_authentication():
    """
    1. Get required data
    2. Call the worker method
    3. Render success response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required data
    args = Eg023IDVAuthenticationController.get_args()
    try:
        # 2: Call the worker method for idv authentication
        results = Eg023IDVAuthenticationController.worker(args)
        envelope_id = results.envelope_id
        app.logger.info(f"Envelope was created. EnvelopeId {envelope_id} ")

        # 3. Render success response
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"The envelope has been created and sent!<br/> Envelope ID {envelope_id}."
        )

    except ApiException as err:
        return process_error(err)


@eg023.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = {
        "account_id": session["ds_account_id"],  # represent your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # represent your {ACCESS_TOKEN}

    }

    workflow_id = Eg023IDVAuthenticationController.get_workflow(args)

    return render_template(
        "eSignature/eg023_idv_authentication.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg023_idv_authentication.py",
        source_url=DS_CONFIG["github_example_url"] + "eg023_idv_authentication.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"],
        workflow_id=workflow_id
    )

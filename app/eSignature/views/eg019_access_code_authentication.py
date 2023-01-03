""" Example 019: Access Code Recipient Authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint, session

from ..examples.eg019_access_code_authentication import Eg019AccessCodeAuthenticationController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 19
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg019 = Blueprint(eg, __name__)

@eg019.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def access_code_authentication():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    args = Eg019AccessCodeAuthenticationController.get_args()
    try:
        # Step 1: Call the worker method for authenticating with access code
        results = Eg019AccessCodeAuthenticationController.worker(args)
        envelope_id = results.envelope_id

        app.logger.info(f"Envelope was created. EnvelopeId {envelope_id} ")

        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"""The envelope has been created and sent!<br/> Envelope ID {envelope_id}."""
        )

    except ApiException as err:
        return process_error(err)


@eg019.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg019_access_code_authentication.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg019_access_code_authentication.py",
        source_url=DS_CONFIG["github_example_url"] + "eg019_access_code_authentication.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

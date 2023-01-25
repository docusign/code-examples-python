""" Example 022: Knowledge Based authentication"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, Blueprint, session

from ..examples.eg022_kba_authentication import Eg022KBAAuthenticationController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 22
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg022 = Blueprint(eg, __name__)


@eg022.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def kba_authentication():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg022KBAAuthenticationController.get_args()
    try:
        # Step 2: Call the worker method for kba
        results = Eg022KBAAuthenticationController.worker(args)
        envelope_id = results.envelope_id
        app.logger.info(f"Envelope was created. EnvelopeId {envelope_id} ")

        # 3. Render success response
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"""The envelope has been created and sent!<br/> Envelope ID {envelope_id}."""
        )

    except ApiException as err:
        return process_error(err)


@eg022.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg022_kba_authentication.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg022_kba_authentication.py",
        source_url=DS_CONFIG["github_example_url"] + "eg022_kba_authentication.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

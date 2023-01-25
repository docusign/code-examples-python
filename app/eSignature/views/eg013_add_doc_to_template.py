"""Example 013: Embedded Signing from template with added document"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint

from ..examples.eg013_add_doc_to_template import Eg013AddDocToTemplateController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 13
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg013 = Blueprint(eg, __name__)


@eg013.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def add_doc_template():
    """
    1. Check the presence of a saved template_id
    2. Get required arguments
    3. Call the worker method
    4. Redirect user to Signing ceremory
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Check the presence of a saved template_id
    if "template_id" in session:
        # 2. Get required arguments
        args = Eg013AddDocToTemplateController.get_args()
        try:
            # 3. Call the worker method
            results = Eg013AddDocToTemplateController.worker(args)
        except ApiException as err:
            return process_error(err)

        # 4. Redirect the user to the embedded signing
        # Don"t use an iFrame!
        # State can be stored/recovered using the framework"s session
        return redirect(results["redirect_url"])

    else:
        return render_template(
            "eSignature/eg013_add_doc_to_template.html",
            title=example["ExampleName"],
            template_ok=False,
            source_file="eg013_add_doc_to_template.py",
            source_url=DS_CONFIG["github_example_url"] + "eg013_add_doc_to_template.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg013.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg013_add_doc_to_template.html",
        title=example["ExampleName"],
        example=example,
        template_ok="template_id" in session,
        source_file="eg013_add_doc_to_template.py",
        source_url=DS_CONFIG["github_example_url"] + "eg013_add_doc_to_template.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

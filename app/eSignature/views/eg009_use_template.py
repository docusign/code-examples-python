"""Example 009: Send envelope using a template"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ...docusign import ensure_manifest, get_example_by_number
from ..examples.eg009_use_template import Eg009UseTemplateController
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 9
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg009 = Blueprint(eg, __name__)


@eg009.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def use_template():
    """
    1. 1. Get required arguments
    2. Call the worker method
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    if "template_id" in session:
        # 1. Get required arguments
        args = Eg009UseTemplateController.get_args()
        try:
            # 1. Call the worker method
            results = Eg009UseTemplateController.worker(args)
        except ApiException as err:
            return process_error(err)

        session["envelope_id"] = results["envelope_id"]  # Save for use by other examples
        # which need an envelopeId
        return render_template(
            "example_done.html",
            title="Envelope sent",
            h1="Envelope sent",
            message=f"""The envelope has been created and sent!<br/>
                    Envelope ID {results["envelope_id"]}.""",
            envelope_ok="envelope_id" in results
        )
    else:
        return render_template(
            "eSignature/eg009_use_template.html",
            title=example["ExampleName"],
            example=example,
            template_ok=False,
            source_file= "eg009_use_template.py",
            source_url=DS_CONFIG["github_example_url"] + "eg009_use_template.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg009.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg009_use_template.html",
        title=example["ExampleName"],
        example=example,
        template_ok="template_id" in session,
        source_file= "eg009_use_template.py",
        source_url=DS_CONFIG["github_example_url"] + "eg009_use_template.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

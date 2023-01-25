""" Example 008: create a template if it doesn"t already exist """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg008_create_template import Eg008CreateTemplateController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 8
api = API_TYPE["ESIGNATURE"]
eg = f"eg00{example_number}"  # reference (and url) for this example
eg008 = Blueprint(eg, __name__)


@eg008.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def create_template():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render template info
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg008CreateTemplateController.get_args()
    try:
        # 2. Call the worker method
        results = Eg008CreateTemplateController.worker(args)
    except ApiException as err:
        return process_error(err)

    # Save the templateId in the session so they can be used in future examples
    session["template_id"] = results["template_id"]
    session["template_ok"] = True

    msg = "The template has been created!" if results["created_new_template"] else \
        "Done. The template already existed in your account."

    # 3. Render template info
    return render_template(
        "example_done.html",
        title="Template results",
        h1="Template results",
        message=f"""{msg}<br/>Template name: {results["template_name"]}, ID {results["template_id"]}."""
    )


@eg008.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg008_create_template.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg008_create_template.py",
        source_url=DS_CONFIG["github_example_url"] + "eg008_create_template.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
    )

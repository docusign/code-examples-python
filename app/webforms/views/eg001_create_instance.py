from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, redirect, url_for

from ..examples.eg001_create_instance import Eg001CreateInstance
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...docusign.utils import replace_template_id
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE, demo_docs_path, web_form_config_file, web_form_template_file

example_number = 1
api = API_TYPE["WEBFORMS"]
eg = f"weg00{example_number}"
weg001 = Blueprint(eg, __name__)


@weg001.route(f"/{eg}", methods=["POST"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def create_web_form_template():
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "template_name": "Web Form Example Template",
        "pdf_file": path.join(demo_docs_path, web_form_template_file)
    }
    try:
        web_form_template_id = Eg001CreateInstance.create_web_form_template(args)
        replace_template_id(path.join(demo_docs_path, web_form_config_file), web_form_template_id)
    except ApiException as error:
        return process_error(error)

    session["web_form_template_id"] = web_form_template_id
    return redirect(url_for(f"{eg}.get_web_form_create_view"))


@weg001.route(f"/{eg}/web_form", methods=["POST"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def create_web_form_instance():
    args = {
        "account_id": session["ds_account_id"],
        "base_path": DS_CONFIG["webforms_api_client_host"],
        "access_token": session["ds_access_token"],
        "client_user_id": "1234-5678-abcd-ijkl",
        "form_name": "Web Form Example Template"
    }

    try:
        forms = Eg001CreateInstance.list_web_forms(args)
        results = Eg001CreateInstance.create_web_form_instance(forms.items[0].id, args)
    except Exception as error:
        return process_error(error)

    return render_template(
        "webforms/eg001_web_form_embed.html",
        form_url=results.form_url,
        instance_token=results.instance_token,
        integration_key=DS_CONFIG["ds_client_id"]
    )


@weg001.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)
    additional_page_data = next((p for p in example["AdditionalPage"] if p["Name"] == "create_web_form_template"),
                                None)
    example["ExampleDescription"] = additional_page_data["ResultsPageText"]

    return render_template(
        "webforms/eg001_create_instance.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg001_create_instance.py",
        source_url=DS_CONFIG["github_example_url"] + "eg001_create_instance.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"]
    )


@weg001.route(f"/{eg}/web_form", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_web_form_create_view():
    if "web_form_template_id" not in session:
        return redirect(url_for(f"{eg}.get_view"))

    example = get_example_by_number(session["manifest"], example_number, api)
    additional_page_data = next((p for p in example["AdditionalPage"] if p["Name"] == "create_web_form"),
                                None)
    return render_template(
        "webforms/eg001_web_form_create.html",
        title=example["ExampleName"],
        example=example,
        description=additional_page_data["ResultsPageText"]
    )

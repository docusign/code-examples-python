from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, redirect, url_for

from ..examples.eg002_create_remote_instance import Eg002CreateRemoteInstance
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...docusign.utils import replace_template_id
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE, demo_docs_path, web_form_config_file, web_form_template_file

example_number = 2
api = API_TYPE["WEBFORMS"]
eg = f"weg00{example_number}"
weg002 = Blueprint(eg, __name__)


@weg002.route(f"/{eg}", methods=["POST"])
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
        web_form_template_id = Eg002CreateRemoteInstance.create_web_form_template(args)
        replace_template_id(path.join(demo_docs_path, web_form_config_file), web_form_template_id)
    except ApiException as error:
        return process_error(error)

    session["web_form_template_id"] = web_form_template_id
    return redirect(url_for(f"{eg}.get_web_form_create_view"))


@weg002.route(f"/{eg}/web_form", methods=["POST"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def create_web_form_instance():
    args = {
        "account_id": session["ds_account_id"],
        "base_path": DS_CONFIG["webforms_api_client_host"],
        "signer_name": DS_CONFIG["signer_name"],
        "signer_email": DS_CONFIG["signer_email"],
        "access_token": session["ds_access_token"],
        "form_name": "Web Form Example Template"
    }

    example = get_example_by_number(session["manifest"], example_number, api)
    try:
        forms = Eg002CreateRemoteInstance.list_web_forms(args)
        if forms.items is None or len(forms.items) == 0:
            error_code = "404"
            error_message = example["CustomErrorTexts"][0]["ErrorMessage"]
            return render_template(
                "error.html",
                error_code=error_code,
                error_message=error_message
            )

        results = Eg002CreateRemoteInstance.create_web_form_instance(forms.items[0].id, args)
    except Exception as error:
        return process_error(error)

    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"].format(results.envelopes[0].id, results.id)
    )


@weg002.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "webforms/eg002_create_remote_instance.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg002_create_remote_instance.py",
        source_url=DS_CONFIG["github_example_url"] + "eg002_create_remote_instance.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"]
    )


@weg002.route(f"/{eg}/web_form", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_web_form_create_view():
    if "web_form_template_id" not in session:
        return redirect(url_for(f"{eg}.get_view"))

    example = get_example_by_number(session["manifest"], example_number, api)
    additional_page_data = next((p for p in example["AdditionalPage"] if p["Name"] == "create_web_form"),
                                None)
    return render_template(
        "webforms/eg002_web_form_create.html",
        title=example["ExampleName"],
        example=example,
        description=additional_page_data["ResultsPageText"].format("app/static/demo_documents")
    )

""" Example 043: Share access to a DocuSign envelope inbox """

import json

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, redirect, current_app, url_for, request

from ..examples.eg043_shared_access import Eg043SharedAccessController
from ...docusign import authenticate, ensure_manifest, get_example_by_number, get_user_info
from ...docusign.utils import ds_logout_internal, authenticate_agent
from ...ds_config import DS_CONFIG, DS_JWT
from ...error_handlers import process_error
from ...consts import pattern, API_TYPE

example_number = 43
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
eg043 = Blueprint(eg, __name__)


@eg043.route(f"/{eg}", methods=["POST"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def create_agent():
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "email": request.form.get("email"),
        "user_name": pattern.sub("", request.form.get("user_name")),
        "activation": pattern.sub("", request.form.get("activation"))
    }
    try:
        # 1. Create the agent user
        results = Eg043SharedAccessController.create_agent(args)
    except ApiException as err:
        return process_error(err)

    session["agent_user_id"] = results.user_id

    example = get_example_by_number(session["manifest"], example_number, api)
    return render_template(
        "example_done.html",
        title="Agent user created",
        message=example["ResultsPageText"],
        json=json.dumps(json.dumps(results.to_dict())),
        redirect_url=f"/{eg}auth"
    )


@eg043.route(f"/{eg}auth", methods=["GET"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def create_authorization():
    user_info = get_user_info(
        session["ds_access_token"],
        session["ds_base_path"],
        DS_CONFIG["authorization_server"].replace("https://", "")
    )
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "user_id": user_info.sub,
        "agent_user_id": session["agent_user_id"]
    }
    try:
        # 2. Create the authorization for agent user
        Eg043SharedAccessController.create_authorization(args)
    except ApiException as err:
        error_body_json = err and hasattr(err, "body") and err.body
        error_body = json.loads(error_body_json)
        error_code = error_body and "errorCode" in error_body and error_body["errorCode"]
        if error_code == "USER_NOT_FOUND":
            example = get_example_by_number(session["manifest"], example_number, api)
            additional_page_data = next((p for p in example["AdditionalPage"] if p["Name"] == "user_not_found"),
                                        None)
            return render_template(
                "example_done.html",
                title="Agent user created",
                message=additional_page_data["ResultsPageText"],
                redirect_url=f"/{eg}auth"
            )

        return process_error(err)

    session["principal_user_id"] = user_info.sub

    example = get_example_by_number(session["manifest"], example_number, api)
    additional_page_data = next((p for p in example["AdditionalPage"] if p["Name"] == "authenticate_as_agent"), None)
    return render_template(
        "example_done.html",
        title="Authenticate as the agent",
        message=additional_page_data["ResultsPageText"],
        redirect_url=f"/{eg}reauthenticate"
    )


@eg043.route(f"/{eg}reauthenticate", methods=["GET"])
def reauthenticate():
    # 3. Logout principal user and redirect to page with the list of envelopes, login as agent user
    ds_logout_internal()
    current_app.config["isLoggedIn"] = False
    return redirect(url_for(f"{eg}.list_envelopes"))


@eg043.route(f"/{eg}envelopes", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate_agent(eg=eg)
def list_envelopes():
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "user_id": session["principal_user_id"]
    }
    try:
        # 4. Retrieve the list of envelopes
        results = Eg043SharedAccessController.get_envelopes(args)
    except ApiException as err:
        return process_error(err)

    example = get_example_by_number(session["manifest"], example_number, api)

    if int(results.result_set_size) > 0:
        additional_page = next((p for p in example["AdditionalPage"] if p["Name"] == "list_status_successful"), None)
        return render_template(
            "example_done.html",
            title="Principal's envelopes visible in the agent's Shared Access UI",
            message=additional_page["ResultsPageText"],
            json=json.dumps(json.dumps(results.to_dict()))
        )

    additional_page = next((p for p in example["AdditionalPage"] if p["Name"] == "list_status_unsuccessful"), None)
    return render_template(
        "example_done.html",
        title="No envelopes in the principal user's account",
        message=additional_page["ResultsPageText"]
    )


@eg043.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg043_shared_access.html",
        title=example["ExampleName"],
        example=example,
        source_file="eg043_shared_access.py",
        source_url=DS_CONFIG["github_example_url"] + "eg043_shared_access.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

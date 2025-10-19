""" Example 045: Delete and undelete an Envelope """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, request, redirect

from ..examples.eg045_delete_restore_envelope import Eg045DeleteRestoreEnvelopeController
from ..utils import get_folder_id_by_name
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import pattern, API_TYPE

example_number = 45
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference (and url) for this example
restore_endpoint = f"{eg}restore"
delete_folder_id = "recyclebin"
restore_folder_id = "sentitems"
eg045 = Blueprint(eg, __name__)

@eg045.route(f"/{eg}", methods=["POST"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def delete_envelope():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    # 1. Get required arguments
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "envelope_id": pattern.sub("", request.form.get("envelope_id")),
        "delete_folder_id": delete_folder_id
    }
    try:
        # 2. Call the worker method
        Eg045DeleteRestoreEnvelopeController.delete_envelope(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = args["envelope_id"]  # Save for use by second part of example

    # 3. Render success response
    example = get_example_by_number(session["manifest"], example_number, api)
    additional_page_data = next(
        (p for p in example["AdditionalPage"] if p["Name"] == "envelope_is_deleted"), 
        None
    )
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=additional_page_data["ResultsPageText"].format(args["envelope_id"]),
        redirect_url=restore_endpoint
    )

@eg045.route(f"/{restore_endpoint}", methods=["POST"])
@authenticate(eg=eg, api=api)
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
def restore_envelope():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response
    """

    # 1. Get required arguments
    folder_name = pattern.sub("", request.form.get("folder_name"))
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "envelope_id": pattern.sub("", session.get("envelope_id")),
        "from_folder_id": delete_folder_id
    }

    example = get_example_by_number(session["manifest"], example_number, api)
    try:
        # 2. Call the worker method
        folders = Eg045DeleteRestoreEnvelopeController.get_folders(args)
        args["folder_id"] = get_folder_id_by_name(folders.folders, folder_name)

        if args["folder_id"] is None:
            additional_page_data = next(
                (p for p in example["AdditionalPage"] if p["Name"] == "folder_does_not_exist"), 
                None
            )

            return render_template(
                "example_done.html",
                title=example["ExampleName"],
                message=additional_page_data["ResultsPageText"].format(folder_name),
                redirect_url=restore_endpoint
            )

        Eg045DeleteRestoreEnvelopeController.move_envelope_to_folder(args)
    except ApiException as err:
        return process_error(err)

    # 3. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title=example["ExampleName"],
        message=example["ResultsPageText"].format(session.get("envelope_id", ""), args["folder_id"], folder_name)
    )

@eg045.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg045_delete_envelope.html",
        title=example["ExampleName"],
        example=example,
        envelope_id=session.get("envelope_id", ""),
        submit_button_text=session["manifest"]["SupportingTexts"]["HelpingTexts"]["SubmitButtonDeleteText"],
        source_file="eg045_delete_restore_envelope.py",
        source_url=DS_CONFIG["github_example_url"] + "eg045_delete_restore_envelope.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

@eg045.route(f"/{restore_endpoint}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_restore_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    if not session.get("envelope_id"):
        return redirect(eg)

    return render_template(
        "eSignature/eg045_restore_envelope.html",
        title=example["ExampleName"],
        example=example,
        envelope_id=session.get("envelope_id"),
        submit_button_text=session["manifest"]["SupportingTexts"]["HelpingTexts"]["SubmitButtonRestoreText"],
        source_file="eg045_delete_restore_envelope.py",
        source_url=DS_CONFIG["github_example_url"] + "eg045_delete_restore_envelope.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

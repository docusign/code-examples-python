"""Example 006: Embed a clickwrap"""

from os import path
import json
import webbrowser

from docusign_click.client.api_exception import ApiException
from flask import render_template, current_app, Blueprint, session

from ..examples.eg006_embed_clickwrap import Eg006EmbedClickwrapController
from ..examples.eg002_activate_clickwrap import Eg002ActivateClickwrapController
from app.docusign import authenticate, get_example_by_number, ensure_manifest
from app.ds_config import DS_CONFIG
from app.error_handlers import process_error

example_number = 6
eg = f"eg00{example_number}"  # Reference (and URL) for this example
eg006 = Blueprint(eg, __name__)


@eg006.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["click_manifest_url"])
@authenticate(eg=eg)
def embed_clickwrap():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number)

    # 1. Get required arguments
    args = Eg006EmbedClickwrapController.get_args()

    try:
        # 2. Call the worker method to create a new clickwrap
        results = Eg006EmbedClickwrapController.worker(args)
        current_app.logger.info(
            f"""See the embedded clickwrap in the dialog box."""
        )
    except ApiException as err:
        return process_error(err)

    # Save for use by other examples which need an clickwrap params.
    session["clickwrap_is_active"] = True

    if results.to_dict()["agreement_url"] == None:
        return render_template(
            "error.html",
            error_code="200",
            error_message="The email address was already used to agree to this elastic template. Provide a different email address if you want to view the agreement and agree to it."
        )

    # 3. Render the response
    return render_template(
        "eg006_done.html",
        title=example["ExampleName"],
        message=f"""See the embedded clickwrap in the dialog box.""",
        json=json.dumps(json.dumps(results.to_dict(), default=str)),
        agreementUrl= results.to_dict()["agreement_url"]
    )


@eg006.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["click_manifest_url"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number)

    args = Eg006EmbedClickwrapController.get_args()
    return render_template(
        "eg006_embed_clickwrap.html",
        title=example["ExampleName"],
        example=example,
        clickwraps_data=Eg006EmbedClickwrapController.get_active_clickwraps(args),
        inactive_clickwraps_data=Eg002ActivateClickwrapController.get_inactive_clickwraps(args),
        source_file= "eg006_embed_clickwrap.py",
        source_url=DS_CONFIG["click_github_url"] + "eg006_embed_clickwrap.py",
    )

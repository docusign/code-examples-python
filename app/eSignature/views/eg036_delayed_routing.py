
""" Example 036: Delayed routing """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, request

from ..examples.eg036_delayed_routing import Eg036DelayedRoutingController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import pattern

eg = "eg036"  # reference (and url) for this example
eg036 = Blueprint("eg036", __name__)

def get_args():
    """Get request and session arguments"""
    
    signer_email = pattern.sub("", request.form.get("signer_email"))
    signer_name = pattern.sub("", request.form.get("signer_name"))
    signer_email2 = pattern.sub("", request.form.get("signer_email2"))
    signer_name2 = pattern.sub("", request.form.get("signer_name2"))
    delay = request.form.get("delay")
    envelope_args = {
        "signer_email": signer_email,
        "signer_name": signer_name,
        "signer_email2": signer_email2,
        "signer_name2": signer_name2,
        "delay": delay,
        "status": "sent",
    }
    args = {
        "account_id": session["ds_account_id"],
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],
        "envelope_args": envelope_args
    }
    return args

@eg036.route("/eg036", methods=["POST"])
@authenticate(eg=eg)
def sign_by_email():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

    # 1. Get required arguments
    args = get_args()
    try:
        # 2. Call the worker method
        results = Eg036DelayedRoutingController.worker(args)
        print(results)
    except ApiException as err:
        return process_error(err)


    # 3. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title="Envelope sent",
        h1="Envelope sent",
        message=f"The envelope has been created and sent!<br/>Envelope ID: {results['envelope_id']}."
    )


@eg036.route("/eg036", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg036_delayed_routing.html",
        title="Scheduled sending",
        source_file="eg036_delayed_routing.py",
        source_url=DS_CONFIG["github_example_url"] + "eg036_delayed_routing.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

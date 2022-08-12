""" Example 039: In Person Signer """

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint, request

from ..examples.eg039_in_person_signer import Eg039InPersonSigner
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import pattern

eg = "eg039"  # reference (and url) for this example
eg039 = Blueprint("eg039", __name__)

# def get_args():
#     """Get request and session arguments"""

#     # More data validation would be a good idea here
#     # Strip anything other than characters listed
#     host_email = pattern.sub("", session.get("host_email"))
#     host_name = pattern.sub("", session.get("host_name"))
#     signer_email = pattern.sub("", session.get("signer_email"))
#     signer_name = pattern.sub("", session.get("signer_name"))
#     envelope_args = {
#         "host_email": host_email,
#         "host_name": host_name,
#         #"signer_email": signer_email,
#         "signer_name": signer_name,
#         "status": "sent",
#     }
#     args = {
#         "account_id": session["ds_account_id"],
#         "base_path": session["ds_base_path"],
#         "access_token": session["ds_access_token"],
#         "envelope_args": envelope_args
#     }
#     return args

@eg039.route("/eg039", methods=["POST"])
@authenticate(eg=eg)
def in_person_signer():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render success response with envelopeId
    """

    # 1. Get required arguments
    args = Eg039InPersonSigner.get_args()
    try:
        # 1. Call the worker method
        results = Eg039InPersonSigner.worker(args)
    except ApiException as err:
        return process_error(err)

    session["envelope_id"] = results["envelope_id"]  # Save for use by other examples which need an envelopeId

    # 2. Render success response with envelopeId
    return render_template(
        "example_done.html",
        title="Envelope sent",
        h1="Envelope sent",
        message=f"The envelope has been created and sent!<br/>Envelope ID {results['envelope_id']}."
    )


@eg039.route("/eg039", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg039_in_person_signer.html",
        title="Signing via email",
        source_file="eg039_in_person_signer.py",
        source_url=DS_CONFIG["github_example_url"] + "eg039_in_person_signer.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        #signer_email=DS_CONFIG["signer_email"]
    )

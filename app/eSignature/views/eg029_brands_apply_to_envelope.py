"""Example 029: Applying a brand to an envelope"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, Blueprint
from ..examples.eg029_brands_apply_to_envelope import Eg029BrandsApplyToEnvelopeController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg029"  # Reference and URL for this example
eg029 = Blueprint("eg029", __name__)

@eg029.route("/eg029", methods=["POST"])
@authenticate(eg=eg)
def brands_apply_to_envelope():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """

    # 1. Get required arguments
    args = Eg029BrandsApplyToEnvelopeController.get_args()
    try:
        # 2. Call the worker method to apply brand to the envelope
        response = Eg029BrandsApplyToEnvelopeController.worker(args)
        envelope_id = response.envelope_id
        app.logger.info(f"Brand has been applied to envelope. Envelope ID: {envelope_id}")

        # 3. Render the response
        return render_template(
            "example_done.html",
            title="The brand applying to the envelope",
            h1="The brand applying to the envelope",
            message=f"The brand has been applied to the envelope!<br/> Envelope ID: {envelope_id}."
        )

    except ApiException as err:
        return process_error(err)


@eg029.route("/eg029", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    args = {
        "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}

    }

    # Get all brands to render in the template
    brands = Eg029BrandsApplyToEnvelopeController.get_brands(args)

    return render_template(
        "eg029_brands_apply_to_envelope.html",
        title="Applying a brand to an envelope",
        source_file=path.basename(path.dirname(__file__)) + "/eg029_brands_apply_to_envelope.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg029_brands_apply_to_envelope.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        brands=brands,
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )
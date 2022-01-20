"""Example 030: Applying a brand and template to an envelope"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, Blueprint
from ..examples.eg030_brands_apply_to_template import Eg030BrandsApplyToTemplateController
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg030"  # Reference and URL for this example
eg030 = Blueprint("eg030", __name__)


@eg030.route("/eg030", methods=["POST"])
@authenticate(eg=eg)
def brands_apply_to_template():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render a response
    """

    # 1. Get required arguments
    args = Eg030BrandsApplyToTemplateController.get_args()
    try:
        # 2: Call the worker method to apply the brand to the template
        response = Eg030BrandsApplyToTemplateController.worker(args)
        envelope_id = response.envelope_id
        app.logger.info(f"The brand and template have been applied to the envelope. Envelope ID: {envelope_id}")

        # 3: Render the response
        return render_template(
            "example_done.html",
            title="Applying a brand and template to an envelope",
            h1="Applying a brand and template to an envelope",
            message=f"The brand and template have been applied to the envelope!<br/> Envelope ID: {envelope_id}."
        )

    except ApiException as err:
        return process_error(err)


@eg030.route("/eg030", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    args = {
        "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
    }
    brands, templates = Eg030BrandsApplyToTemplateController.get_data(args)
    return render_template(
        "eg030_brands_apply_to_template.html",
        title="Applying a brand and template to an envelope",
        source_file= "eg030_brands_apply_to_template.py",
        source_url=DS_CONFIG["github_example_url"] + "eg030_brands_apply_to_template.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        brands=brands,
        templates=templates,
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"],
    )
"""Example 030: Applying a brand and template to an envelope"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, Blueprint

from ..examples.eg030_brands_apply_to_template import Eg030BrandsApplyToTemplateController
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 30
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # Reference and URL for this example
eg030 = Blueprint(eg, __name__)


@eg030.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def brands_apply_to_template():
    """
    1. Check the presence of a saved template_id
    2. Get required arguments
    3. Call the worker method
    4. Render a response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Check the presence of a saved template_id
    if "template_id" in session:
        # 2. Get required arguments
        args = Eg030BrandsApplyToTemplateController.get_args()
        try:
            # 3: Call the worker method to apply the brand to the template
            response = Eg030BrandsApplyToTemplateController.worker(args)
            envelope_id = response.envelope_id
            app.logger.info(f"The brand and template have been applied to the envelope. Envelope ID: {envelope_id}")

            # 4: Render the response
            return render_template(
                "example_done.html",
                title=example["ExampleName"],
                message=f"The brand and template have been applied to the envelope!<br/> Envelope ID: {envelope_id}."
            )

        except ApiException as err:
            return process_error(err)
    
    else:
        return render_template(
            "eSignature/eg030_brands_apply_to_template.html",
            title=example["ExampleName"],
            example=example,
            template_ok=False,
            source_file= "eg030_brands_apply_to_template.py",
            source_url=DS_CONFIG["github_example_url"] + "eg030_brands_apply_to_template.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg030.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    args = {
        "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
        "base_path": session["ds_base_path"],
        "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
    }
    brands = Eg030BrandsApplyToTemplateController.get_data(args)
    return render_template(
        "eSignature/eg030_brands_apply_to_template.html",
        title=example["ExampleName"],
        example=example,
        template_ok="template_id" in session,
        source_file= "eg030_brands_apply_to_template.py",
        source_url=DS_CONFIG["github_example_url"] + "eg030_brands_apply_to_template.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        brands=brands,
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"],
    )
"""Example 028: Creating a brand"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, request, Blueprint

from ..examples.eg028_brand_creating import Eg028BrandCreatingController
from ...consts import languages
from ...docusign import authenticate, ensure_manifest, get_example_by_number
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error
from ...consts import API_TYPE

example_number = 28
api = API_TYPE["ESIGNATURE"]
eg = f"eg0{example_number}"  # reference and url for this example
eg028 = Blueprint(eg, __name__)

@eg028.route(f"/{eg}", methods=["POST"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def brand_creating():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """
    example = get_example_by_number(session["manifest"], example_number, api)

    # 1. Get required arguments
    args = Eg028BrandCreatingController.get_args()
    try:
        # 2. Call the worker method to create a new brand
        response = Eg028BrandCreatingController.worker(args)
        brand_id = response.brands[0].brand_id
        app.logger.info(f"Brand has been created. Brand ID: {brand_id}")

        # 3. Render the response
        return render_template(
            "example_done.html",
            title=example["ExampleName"],
            message=f"""The brand has been created and sent!<br/> Brand ID: {brand_id}."""
        )

    except ApiException as err:
        return process_error(err)

@eg028.route(f"/{eg}", methods=["GET"])
@ensure_manifest(manifest_url=DS_CONFIG["example_manifest_url"])
@authenticate(eg=eg, api=api)
def get_view():
    """Responds with the form for the example"""
    example = get_example_by_number(session["manifest"], example_number, api)

    return render_template(
        "eSignature/eg028_brand_creating.html",
        title=example["ExampleName"],
        example=example,
        source_file= "eg028_brand_creating.py",
        source_url=DS_CONFIG["github_example_url"] + "eg028_brand_creating.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        languages=languages
    )
"""Example 028: Creating a brand"""

from os import path
from docusign_esign.client.api_exception import ApiException
from flask import current_app as app
from flask import render_template, session, request, Blueprint
from ..examples.eg028_brand_creating import Eg028BrandCreatingController
from ...consts import languages
from ...docusign import authenticate
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg028"  # reference and url for this example
eg028 = Blueprint("eg028", __name__)

@eg028.route("/eg028", methods=["POST"])
@authenticate(eg=eg)
def brand_creating():
    """
    1. Get required arguments
    2. Call the worker method
    3. Render the response
    """

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
            title="Brand creating",
            h1="Brand creating",
            message=f"""The brand has been created and sent!<br/> Brand ID: {brand_id}."""
        )

    except ApiException as err:
        return process_error(err)

@eg028.route("/eg028", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """Responds with the form for the example"""

    return render_template(
        "eg028_brand_creating.html",
        title="Brand creating",
        source_file= "eg028_brand_creating.py",
        source_url=DS_CONFIG["github_example_url"] + "eg028_brand_creating.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        languages=languages
    )
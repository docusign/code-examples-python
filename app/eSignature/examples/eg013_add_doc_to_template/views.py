"""Example 013: Embedded Signing from template with added document"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, redirect, session, Blueprint

from .controller import Eg013Controller
from ....docusign import authenticate
from ....ds_config import DS_CONFIG
from ....error_handlers import process_error

eg = "eg013"  # reference (and url) for this example
eg013 = Blueprint("eg013", __name__)


@eg013.route("/eg013", methods=["POST"])
@authenticate(eg=eg)
def add_doc_template():
    """
    1. Check the presence of a saved template_id
    2. Get required arguments
    3. Call the worker method
    4. Redirect user to Signing ceremory
    """
    # 1. Check the presence of a saved template_id
    if "template_id" in session:
        # 2. Get required arguments
        args = Eg013Controller.get_args()
        try:
            # 3. Call the worker method
            results = Eg013Controller.worker(args)
        except ApiException as err:
            return process_error(err)

        # 4. Redirect the user to the embedded signing
        # Don"t use an iFrame!
        # State can be stored/recovered using the framework"s session
        return redirect(results["redirect_url"])

    else:
        return render_template(
            "eg013_add_doc_to_template.html",
            title="Use embedded signing from template and extra doc",
            template_ok=False,
            source_file=path.basename(path.dirname(__file__)) + "/controller.py",
            source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg013.route("/eg013", methods=["GET"])
@authenticate(eg=eg)
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg013_add_doc_to_template.html",
        title="Use embedded signing from template and extra doc",
        template_ok="template_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/controller.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

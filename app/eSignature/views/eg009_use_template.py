"""Example 009: Send envelope using a template"""

from os import path

from docusign_esign.client.api_exception import ApiException
from flask import render_template, session, Blueprint

from ..examples.eg009_use_template import Eg009UseTemplateController
from ...ds_config import DS_CONFIG
from ...error_handlers import process_error

eg = "eg009"  # reference (and url) for this example
eg009 = Blueprint("eg009", __name__)


@eg009.route("/eg009", methods=["POST"])
def use_template():
    """
    1. 1. Get required arguments
    2. Call the worker method
    """

    if "template_id" in session:
        # 1. Get required arguments
        args = Eg009UseTemplateController.get_args()
        try:
            # 1. Call the worker method
            results = Eg009UseTemplateController.worker(args)
        except ApiException as err:
            return process_error(err)

        session["envelope_id"] = results["envelope_id"]  # Save for use by other examples
        # which need an envelopeId
        return render_template(
            "example_done.html",
            title="Envelope sent",
            h1="Envelope sent",
            message=f"""The envelope has been created and sent!<br/>
                    Envelope ID {results["envelope_id"]}.""",
            envelope_ok="envelope_id" in results
        )
    else:
        return render_template(
            "eg009_use_template.html",
            title="Use a template to send an envelope",
            template_ok=False,
            source_file=path.basename(path.dirname(__file__)) + "/eg009_use_template.py",
            source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg009_use_template.py",
            documentation=DS_CONFIG["documentation"] + eg,
            show_doc=DS_CONFIG["documentation"],
        )


@eg009.route("/eg009", methods=["GET"])
def get_view():
    """responds with the form for the example"""

    return render_template(
        "eg009_use_template.html",
        title="Use a template to send an envelope",
        template_ok="template_id" in session,
        source_file=path.basename(path.dirname(__file__)) + "/eg009_use_template.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(path.dirname(__file__)) + "/eg009_use_template.py",
        documentation=DS_CONFIG["documentation"] + eg,
        show_doc=DS_CONFIG["documentation"],
        signer_name=DS_CONFIG["signer_name"],
        signer_email=DS_CONFIG["signer_email"]
    )

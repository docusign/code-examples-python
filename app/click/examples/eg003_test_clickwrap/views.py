"""Example 003: Testing a clickwrap"""

from os import path

from flask import render_template, Blueprint, session

from .controller import Eg003Controller
from app.docusign import authenticate
from app.ds_config import DS_CONFIG

eg = "eg003"  # Reference (and URL) for this example
eg003 = Blueprint("eg003", __name__)


@eg003.route("/eg003", methods=["GET"])
@authenticate(eg=eg)
def test_clickwrap():
    """responds with the form for the example"""
    # 1. Get required arguments
    args = Eg003Controller.get_args()

    # 2. Render template
    return render_template(
        "eg003_test_clickwrap.html",
        title="Testing a clickwrap",
        clickwrap_ok=session.get("clickwrap_id") and session.get("clickwrap_is_active"),
        clickwrap_test_url=f"https://developers.docusign.com/docs/click-api/"
                           f"test-clickwrap?a={args['account_id']}"
                           f"&cw={args['clickwrap_id']}&eh=demo",
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(
            path.dirname(__file__)) + "/controller.py",
    )

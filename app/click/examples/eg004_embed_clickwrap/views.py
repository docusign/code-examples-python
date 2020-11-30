"""Example 004: Embeding a clickwrap"""

from os import path

from flask import request, render_template, Blueprint, session

from .controller import Eg004Controller
from app.docusign import authenticate
from app.ds_config import DS_CONFIG

eg = "eg004"  # reference (and url) for this example
eg004 = Blueprint("eg004", __name__)


@eg004.route("/eg004", methods=["GET", "POST"])
@authenticate(eg=eg)
def embed_clickwrap():
    """
    1. Get required arguments
    2. Render the response
    """
    # 1. Get required arguments
    args = Eg004Controller.get_args()
    show_clickwrap = True if request.method == 'POST' else False

    # 2. Render template
    return render_template(
        "eg004_embed_clickwrap.html",
        title="Embeding a clickwrap",
        account_id=args.get('account_id'),
        client_user_id=DS_CONFIG.get('signer_email'),
        clickwrap_id=args.get('clickwrap_id'),
        clickwrap_ok=session.get("clickwrap_id") and session.get("clickwrap_is_active"),
        show_clickwrap=show_clickwrap,
        source_file=path.basename(path.dirname(__file__)) + "/controller.py",
        source_url=DS_CONFIG["github_example_url"] + path.basename(
            path.dirname(__file__)) + "/controller.py",
    )

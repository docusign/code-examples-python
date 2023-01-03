"""Defines the home page route"""

from flask import (
    render_template,
    url_for,
    redirect,
    Blueprint,
    session,
    current_app as app
)

from .ds_config import DS_CONFIG
from .api_type import EXAMPLES_API_TYPE
from .docusign import get_manifest

core = Blueprint("core", __name__)


@core.route("/")
def index():
    session["manifest"] = get_manifest(DS_CONFIG["example_manifest_url"])

    if DS_CONFIG["quickstart"] == "true":
        app.config["quickstart"] = False
        return redirect(url_for("eg001.get_view"))
    if "is_cfr" in session and session["is_cfr"] == "enabled":
        return render_template("cfr_home.html", title="Home - Python Code Examples", manifest=session["manifest"], crfEnabled="True")
    else:
        return render_template("home.html", title="Home - Python Code Examples", manifest=session["manifest"], crfEnabled="False")


@core.route("/index")
def r_index():
    return redirect(url_for("core.index"))


@core.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@core.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

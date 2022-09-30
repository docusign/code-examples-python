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
    if EXAMPLES_API_TYPE["Rooms"]:
        session["manifest"] = get_manifest(DS_CONFIG["rooms_manifest_url"])
        return render_template(
            "home_rooms.html", title="Home - Python Rooms API Code Examples", manifest=session["manifest"]
        )
    elif EXAMPLES_API_TYPE["Click"]:
        session["manifest"] = get_manifest(DS_CONFIG["click_manifest_url"])
        return render_template(
            "home_click.html", title="Home - Python Click API Code Examples", manifest=session["manifest"]
        )
    elif EXAMPLES_API_TYPE["Monitor"]:
        session["manifest"] = get_manifest(DS_CONFIG["monitor_manifest_url"])
        return render_template(
            "home_monitor.html",
            title="Home - Python Monitor API Code Examples", manifest=session["manifest"]
        )
    elif EXAMPLES_API_TYPE["Admin"]:
        session["manifest"] = get_manifest(DS_CONFIG["admin_manifest_url"])
        return render_template(
            "home_admin.html",
            title="Home - Python Admin API Code Examples", manifest=session["manifest"]
        )
    else:
        session["manifest"] = get_manifest(DS_CONFIG["esign_manifest_url"])

    if DS_CONFIG["quickstart"] == "true":
        app.config["quickstart"] = False
        return redirect(url_for("eg001.get_view"))
        
    else:
        return render_template("home.html", title="Home - Python Code Examples", manifest=session["manifest"])


@core.route("/index")
def r_index():
    return redirect(url_for("core.index"))


@core.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@core.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

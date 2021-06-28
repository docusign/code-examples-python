"""Defines the home page route"""

from flask import (
    render_template,
    url_for,
    redirect,
    Blueprint,
    current_app as app
)

from .ds_config import DS_CONFIG
from .ds_config import EXAMPLES_API_TYPE

core = Blueprint("core", __name__)


@core.route("/")
def index():
    if EXAMPLES_API_TYPE["Rooms"]:
        return render_template(
            "home_rooms.html", title="Home - Python Rooms API Code Examples"
        )
    elif EXAMPLES_API_TYPE["Click"]:
        return render_template(
            "home_click.html", title="Home - Python Click API Code Examples"
        )

    elif EXAMPLES_API_TYPE["Monitor"]:
        return render_template(
            "home_monitor.html",
            title="Home - Python Monitor API Code Examples"
        )
    elif EXAMPLES_API_TYPE["Admin"]:
        return render_template(
            "home_admin.html",
            title="Home - Python Admin API Code Examples"
        )

    if DS_CONFIG["quickstart"] == "true":
        app.config["quickstart"] = False
        return redirect(url_for("eg001.get_view"))
        
    else:
        return render_template("home.html", title="Home - Python Code Examples")


@core.route("/index")
def r_index():
    return redirect(url_for("core.index"))


@core.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@core.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

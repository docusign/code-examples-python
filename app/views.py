"""Defines the home page route"""

from flask import render_template, url_for, redirect, Blueprint, current_app as app
from .ds_config import DS_CONFIG

core = Blueprint("core", __name__)


@core.route("/")
def index():
    #if quickstart go to eg001 else go to homepage
    quickstart=app.config["quickstart"]
    if quickstart  == True:
        return render_template("eg001_embedded_signing.html", title="Embedded signing ceremony")
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

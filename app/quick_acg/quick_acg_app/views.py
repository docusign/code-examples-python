"""Defines the home page route"""
from datetime import datetime, timedelta

from flask import (
    url_for,
    redirect,
    Blueprint,
    session,
    request,
    flash,
    current_app as app
)

from app.docusign.ds_client import DSClient
from app.docusign.utils import is_cfr
from app.consts import base_uri_suffix
from app.ds_config import DS_CONFIG

ds = Blueprint("ds", __name__, url_prefix="/ds")

@ds.route("/login", methods=["GET", "POST"])
def ds_login():
    if not session.get("auth_type"):
        session["auth_type"] = request.form.get("auth_type")
    app.config["isLoggedIn"] = True
    return DSClient.login("code_grant", session.get("api"))

@ds.route("/callback")
def ds_callback():
    """
    Save the token information in session.
    Call api to get user's information if it doesn't present
    """

    # Save the redirect eg if present
    redirect_url = session.pop("eg", None)
    resp = DSClient.get_token("code_grant")

    # app.logger.info("Authenticated with DocuSign.")
    session["ds_access_token"] = resp["access_token"]
    session["ds_refresh_token"] = resp["refresh_token"]
    session["ds_expiration"] = datetime.utcnow() + timedelta(seconds=int(resp["expires_in"]))

    if not session.get("ds_account_id"):
        flash("You have authenticated with DocuSign.")
        # Request to API to get the user information
        response = DSClient.get_user(session["ds_access_token"])
        session["ds_user_name"] = response["name"]
        session["ds_user_email"] = response["email"]
        accounts = response["accounts"]
        # Find the account...
        target_account_id = DS_CONFIG["target_account_id"]
        if target_account_id:
            account = next((a for a in accounts if a["account_id"] == target_account_id), None)
            if not account:
                # The user does not have the targeted account. They should not log in!
                raise Exception(f"No access to target account with ID: {target_account_id}")
        else:  # get the default account
            account = next((a for a in accounts if a["is_default"]), None)
            if not account:
                # Every user should always have a default account
                raise Exception("No default account. Every user should always have a default account")

        # Save the account information
        session["ds_account_id"] = account["account_id"]
        session["ds_account_name"] = account["account_name"]
        session["ds_base_path"] = account["base_uri"] + base_uri_suffix

    session["is_cfr"] = is_cfr(session["ds_access_token"], session["ds_account_id"], session["ds_base_path"])

    if not redirect_url:
        redirect_url = url_for("core.index")
    return redirect(redirect_url)

@ds.route("/must_authenticate")
def ds_must_authenticate():
    session["auth_type"] = "code_grant"
    return redirect(url_for("ds.ds_login"))

@ds.route("/logout")
def ds_logout():
    flash("You have logged out from DocuSign.")
    app.config["isLoggedIn"] = False
    app.config["quickstart"] = False

    return redirect(url_for("core.index"))

@ds.route("/ds_return")
def ds_return():
    return redirect(url_for("core.index"))

core = Blueprint("core", __name__)

@core.route("/")
def index():
    return redirect(url_for("eg001.get_view"))

@core.route("/index")
def r_index():
    return redirect(url_for("core.index"))

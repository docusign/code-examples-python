from datetime import datetime, timedelta

from flask import redirect, request, url_for, flash, render_template, Blueprint, session, current_app as app

from .ds_client import DSClient
from .utils import ds_logout_internal
from ..consts import base_uri_suffix
from ..ds_config import DS_CONFIG
from ..ds_config import EXAMPLES_API_TYPE

ds = Blueprint("ds", __name__, url_prefix="/ds")


@ds.route("/login", methods=["GET", "POST"])
def ds_login():
    if not session.get("auth_type"):
        session["auth_type"] = request.form.get("auth_type")
    app.config["isLoggedIn"] = True
    app.config["quickstart"] = DS_CONFIG["quickstart"]
    return DSClient.login(session["auth_type"])


@ds.route("/logout")
def ds_logout():
    ds_logout_internal()
    flash("You have logged out from DocuSign.")
    app.config["isLoggedIn"] = False
    app.config["quickstart"] = False
    return redirect(url_for("core.index"))


@ds.route("/callback")
def ds_callback():
    """
    Save the token information in session.
    Call api to get user's information if it doesn't present
    """

    # Save the redirect eg if present
    redirect_url = session.pop("eg", None)
    resp = DSClient.get_token(session["auth_type"])

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
                raise Exception("No access to target account")
        else:  # get the default account
            account = next((a for a in accounts if a["is_default"]), None)
            if not account:
                # Every user should always have a default account
                raise Exception("No default account")

        # Save the account information
        session["ds_account_id"] = account["account_id"]
        session["ds_account_name"] = account["account_name"]
        session["ds_base_path"] = account["base_uri"] + base_uri_suffix

    if not redirect_url:
        redirect_url = url_for("core.index")
    return redirect(redirect_url)


@ds.route("/must_authenticate")
def ds_must_authenticate():
    if DS_CONFIG["quickstart"] == "true" and EXAMPLES_API_TYPE['ESignature']:
        session["auth_type"] = "code_grant"
        return redirect(url_for("ds.ds_login"))

    elif EXAMPLES_API_TYPE["Monitor"] or EXAMPLES_API_TYPE["Admin"]:
        session["auth_type"] = "jwt"
        return redirect(url_for("ds.ds_login"))

    else:
        return render_template("must_authenticate.html", title="Must authenticate")


@ds.route("/ds_return")
def ds_return():
    event = request.args.get("event")
    state = request.args.get("state")
    envelope_id = request.args.get("envelopeId")
    DS_CONFIG["quickstart"] = "false"
    return render_template(
        "ds_return.html",
        title="Return from DocuSign",
        event=event,
        envelope_id=envelope_id,
        state=state
    )

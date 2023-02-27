from datetime import datetime, timedelta

from flask import redirect, request, url_for, flash, render_template, Blueprint, session, current_app as app

import json
from .ds_client import DSClient
from .utils import ds_logout_internal, get_manifest, is_cfr
from ..consts import base_uri_suffix
from ..ds_config import DS_CONFIG
from ..api_type import EXAMPLES_API_TYPE

ds = Blueprint("ds", __name__, url_prefix="/ds")
manifest_url = DS_CONFIG["example_manifest_url"]

@ds.route("/login", methods=["GET", "POST"])
def ds_login():
    if session.get('manifest'):
        session.pop('manifest')

    if not session.get("auth_type"):
        session["auth_type"] = request.form.get("auth_type")

    session["manifest"] = get_manifest(manifest_url)

    app.config["isLoggedIn"] = True
    app.config["quickstart"] = DS_CONFIG["quickstart"]
    return DSClient.login(session["auth_type"], session.get("api"))


@ds.route("/logout")
def ds_logout():
    ds_logout_internal()
    flash("You have logged out from DocuSign.")
    app.config["isLoggedIn"] = False
    app.config["quickstart"] = False

    return redirect(url_for("core.index"))

@ds.route("/choose_api")
def choose_api():
    session["manifest"] = get_manifest(manifest_url)
    return render_template("choose_api.html", title="Choose API", manifest=session["manifest"])

@ds.route("/api_selected", methods=["GET", "POST"])
def api_selected():
    chosen_api = request.form.get("chosen_api")

    new_api_type = EXAMPLES_API_TYPE

    # Set all values to False
    for api_type in new_api_type:
        if new_api_type[api_type] == True:
            new_api_type[api_type] = False

    # Update the new chosen API type to True
    if chosen_api == "ESignature":
        new_api_type["ESignature"] = True
    elif chosen_api == "Rooms":
        new_api_type["Rooms"] = True
    elif chosen_api == "Admin":
        new_api_type["Admin"] = True
    elif chosen_api == "Monitor":
        new_api_type["Monitor"] = True
    elif chosen_api == "Click":
        new_api_type["Click"] = True 

    # Overwrite api_type.py file
    with open("app/api_type.py", "w") as api_type_file:
        api_type_file.write("EXAMPLES_API_TYPE =" + str(new_api_type))

    ds_logout_internal()
    flash("You have logged out from DocuSign.")
    app.config["isLoggedIn"] = False
    app.config["quickstart"] = False

    session["manifest"] = get_manifest(manifest_url)
    return render_template("must_authenticate.html", title="Must authenticate", chosen_api=chosen_api, manifest=session["manifest"])


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

    if EXAMPLES_API_TYPE["ESignature"] == "true":
        session["is_cfr"] = is_cfr(session["ds_access_token"], session["ds_account_id"], session["ds_base_path"])

    if not redirect_url:
        redirect_url = url_for("core.index")
    return redirect(redirect_url)


@ds.route("/must_authenticate")
def ds_must_authenticate():
    if DS_CONFIG["quickstart"] == "true" and EXAMPLES_API_TYPE["ESignature"]:
        session["auth_type"] = "code_grant"
        return redirect(url_for("ds.ds_login"))

    elif EXAMPLES_API_TYPE["Monitor"]:
        session["auth_type"] = "jwt"
        return redirect(url_for("ds.ds_login"))

    else:
        session["manifest"] = get_manifest(manifest_url)
        return render_template("must_authenticate.html", title="Must authenticate", manifest=session["manifest"])


@ds.route("/ds_return")
def ds_return():
    event = request.args.get("event")
    state = request.args.get("state")
    envelope_id = request.args.get("envelopeId")
    DS_CONFIG["quickstart"] = "false"

    session["manifest"] = get_manifest(manifest_url)
    return render_template(
        "ds_return.html",
        title="Return from DocuSign",
        event=event,
        envelope_id=envelope_id,
        state=state,
        manifest=session["manifest"]
    )
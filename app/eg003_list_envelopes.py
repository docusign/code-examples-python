"""Example 003: List envelopes in the user's account"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
from app import app, ds_config, views
from datetime import datetime, timedelta
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg003"  # reference (and url) for this example

def controller():
    """Controller router using the HTTP method"""
    if request.method == "GET":
        return get_controller()
    elif request.method == "POST":
        return create_controller()
    else:
        return render_template("404.html"), 404


def create_controller():
    """
    1. Check the token
    2. Call the worker method
    3. Show results
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):
        # 2. Call the worker method
        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "ds_access_token": session["ds_access_token"],
        }

        try:
            results = worker(args)
        except ApiException as err:
            error_body_json = err and hasattr(err, "body") and err.body
            # we can pull the DocuSign error code and message from the response body
            error_body = json.loads(error_body_json)
            error_code = error_body and "errorCode" in error_body and error_body["errorCode"]
            error_message = error_body and "message" in error_body and error_body["message"]
            # In production, may want to provide customized error messages and
            # remediation advice to the user.
            return render_template("error.html",
                                   err=err,
                                   error_code=error_code,
                                   error_message=error_message
                                   )
        return render_template("example_done.html",
                                title="List envelopes results",
                                h1="List envelopes results",
                                message="Results from the Envelopes::listStatusChanges method:",
                                json=json.dumps(json.dumps(results.to_dict()))
                                )
    else:
        flash("Sorry, you need to re-authenticate.")
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we"ll make the user re-enter the form data after
        # authentication.
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


# ***DS.snippet.0.start
def worker(args):
    """
    1. Call the envelope status change method to list the envelopes
       that have changed in the last 10 days
    """

    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args["base_path"]
    api_client.set_default_header("Authorization", "Bearer " + args["ds_access_token"])
    envelope_api = EnvelopesApi(api_client)

    # The Envelopes::listStatusChanges method has many options
    # See https://developers.docusign.com/esign-rest-api/reference/Envelopes/Envelopes/listStatusChanges

    # The list status changes call requires at least a from_date OR
    # a set of envelopeIds. Here we filter using a from_date.
    # Here we set the from_date to filter envelopes for the last month
    # Use ISO 8601 date format
    from_date = (datetime.utcnow() - timedelta(days=10)).isoformat()
    results = envelope_api.list_status_changes(args["account_id"], from_date = from_date)

    return results
# ***DS.snippet.0.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg003_list_envelopes.html",
                               title="List changed envelopes",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


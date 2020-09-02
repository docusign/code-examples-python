"""011: Embedded sending: Remote signer, cc, envelope has three documents"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
import re
from app import app, ds_config, views, eg002_signing_via_email
from docusign_esign import *
from docusign_esign import ApiException

eg = "eg011"  # reference (and url) for this example

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
    token_ok = views.ds_token_ok(minimum_buffer_min)
    if token_ok:
        # 2. Call the worker method
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        pattern = re.compile("([^\w \-\@\.\,])+")
        signer_email  = pattern.sub("", request.form.get("signer_email"))
        signer_name   = pattern.sub("", request.form.get("signer_name"))
        cc_email      = pattern.sub("", request.form.get("cc_email"))
        cc_name       = pattern.sub("", request.form.get("cc_name"))
        starting_view = pattern.sub("", request.form.get("starting_view"))

        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "cc_email": cc_email,
            "cc_name": cc_name,
            "status": "sent",
        }
        args = {
            "starting_view": starting_view,
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "ds_access_token": session["ds_access_token"],
            "envelope_args": envelope_args,
            "ds_return_url": url_for("ds_return", _external=True),
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
        if results:
            # Redirect the user to the NDSE view
            # Don't use an iFrame!
            # State can be stored/recovered using the framework's session or a
            # query parameter on the returnUrl (see the makeRecipientViewRequest method)
            return redirect(results["redirect_url"])

    elif not token_ok:
        flash("Sorry, you need to re-authenticate.")
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after
        # authentication.
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))
    elif not "envelope_id" in session:
        return render_template("eg011_embedded_sending.html",
                               title="Embedded Sending",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               )


# ***DS.snippet.0.start
def worker(args):
    """
    This function does the work of creating the envelope in
    draft mode and returning a URL for the sender's view
    """

    # Step 1. Create the envelope with "created" (draft) status
    args["envelope_args"]["status"] = "created"
    # Using worker from example 002
    results = eg002_signing_via_email.worker(args)
    envelope_id = results["envelope_id"]

    # Step 2. Create the sender view
    view_request = ReturnUrlRequest(return_url=args["ds_return_url"])
    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args["base_path"]
    api_client.set_default_header("Authorization", "Bearer " + args["ds_access_token"])
    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_sender_view(args["account_id"], envelope_id, return_url_request=view_request)

    # Switch to Recipient and Documents view if requested by the user
    url = results.url
    if args["starting_view"] == "recipient":
        url = url.replace("send=1", "send=0")

    return {"envelope_id": envelope_id, "redirect_url": url}
# ***DS.snippet.0.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg011_embedded_sending.html",
                               title="Embedded Sending",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               signer_name=ds_config.DS_CONFIG["signer_name"],
                               signer_email=ds_config.DS_CONFIG["signer_email"]
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))

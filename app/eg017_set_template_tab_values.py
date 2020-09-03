"""Example 017: Set Template Tab Values"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
from app import app, ds_config, views
import base64
import re
from docusign_esign import *
from docusign_esign import ApiException

eg = "eg017"  # reference (and url) for this example
signer_client_id = 1000 # Used to indicate that the signer will use an embedded
                        # Signing Ceremony. Represents the signer's userId within
                        # your application.
authentication_method = "None" # How is this application authenticating
                               # the signer? See the "authenticationMethod" definition
                               # https://developers.docusign.com/esign-rest-api/reference/Envelopes/EnvelopeViews/createRecipient

demo_docs_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), "static/demo_documents"))

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
    3. Redirect the user to the signing ceremony
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):
        # 2. Call the worker method
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        pattern = re.compile("([^\w \-\@\.\,])+")
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name  = pattern.sub("", request.form.get("signer_name"))
        cc_email     = pattern.sub("", request.form.get("cc_email"))
        cc_name      = pattern.sub("", request.form.get("cc_name"))
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "signer_client_id": signer_client_id,
            "ds_return_url": url_for("ds_return", _external=True),
            "cc_email" : cc_email,
            "cc_name" : cc_name
        }
        args = {
            "account_id": session["ds_account_id"],
            "base_path": session["ds_base_path"],
            "ds_access_token": session["ds_access_token"],
            "envelope_args": envelope_args
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
            session["envelope_id"] = results["envelope_id"] # Save for use by other examples
                                                            # which need an envelopeId
            # Redirect the user to the Signing Ceremony
            # Don't use an iFrame!
            # State can be stored/recovered using the framework's session or a
            # query parameter on the returnUrl (see the makeRecipientViewRequest method)
            return redirect(results["redirect_url"])

    else:
        flash("Sorry, you need to re-authenticate.")
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after
        # authentication.
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))

# ***DS.snippet.0.start
def worker(args):
    """
    1. Create the envelope request object
    2. Send the envelope
    3. Create the Recipient View request object
    4. Obtain the recipient_view_url for the signing ceremony
    """
    envelope_args = args["envelope_args"]
    # 1. Create the envelope request object
    envelope_definition = make_envelope(envelope_args)

    # 2. call Envelopes::create API method
    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args["base_path"]
    api_client.set_default_header("Authorization", "Bearer " + args["ds_access_token"])

    envelopes_api = EnvelopesApi(api_client)
    results = envelopes_api.create_envelope(args["account_id"], envelope_definition=envelope_definition)
    
    envelope_id = results.envelope_id
    app.logger.info(f"Envelope was created. EnvelopeId {envelope_id}")

    # 3. Create the Recipient View request object
    recipient_view_request = RecipientViewRequest(
        authentication_method = authentication_method,
        client_user_id = envelope_args["signer_client_id"],
        recipient_id = "1",
        return_url = envelope_args["ds_return_url"],
        user_name = envelope_args["signer_name"], email = envelope_args["signer_email"]
    )
    # 4. Obtain the recipient_view_url for the signing ceremony
    # Exceptions will be caught by the calling function
    results = envelopes_api.create_recipient_view(args["account_id"], envelope_id,
        recipient_view_request = recipient_view_request)
    return {"envelope_id": envelope_id, "redirect_url": results.url}

def make_envelope(args):
    """
    Creates envelope
    args -- parameters for the envelope:
    signer_email, signer_name, signer_client_id
    returns an envelope definition
    """

    # Set the values for the fields in the template
    # List item
    list1 = List(
        value = "green", document_id= "1",
        page_number= "1", tab_label= "list" )

    # Checkboxes
    check1 = Checkbox(
        tab_label= "ckAuthorization", selected = "true" )
    
    check3 = Checkbox(
        tab_label= "ckAgreement", selected = "true" )

    radio_group = RadioGroup(
        group_name = "radio1",
        radios = [ Radio( value = "white", selected = "true") ]
    )

    text = Text(
        tab_label = "text", value = "Jabberywocky!"
    )

    # We can also add a new tab (field) to the ones already in the template:
    text_extra = Text(
        document_id = "1", page_number = "1",
        x_position = "280", y_position = "172",
        font = "helvetica", font_size = "size14",
        tab_label = "added text field", height = "23",
        width = "84", required = "false",
        bold = "true", value = args["signer_name"],
        locked = "false", tab_id = "name"
    )

    # Add the tabs model (including the SignHere tab) to the signer.
    # The Tabs object wants arrays of the different field/tab types
    # Tabs are set per recipient / signer
    tabs = Tabs(
        checkbox_tabs = [check1, check3], radio_group_tabs = [radio_group],
        text_tabs = [text, text_extra], list_tabs = [list1]
    )

    # create a signer recipient to sign the document, identified by name and email
    # We"re setting the parameters via the object creation
    signer = TemplateRole( # The signer
        email = args["signer_email"], name = args["signer_name"],
        # Setting the client_user_id marks the signer as embedded
        client_user_id = args["signer_client_id"],
        role_name = "signer",
        tabs = tabs
    )

    cc = TemplateRole(
        email = args["cc_email"],
        name = args["cc_name"],
        role_name="cc"
    )

    # create an envelope custom field to save our application's 
    # data about the envelope

    custom_field = TextCustomField(
        name="app metadata item",
        required="false",
        show="true", # Yes, include in the CoC
        value="1234567"
    )

    cf = CustomFields(text_custom_fields=[custom_field])

    # Next, create the top level envelope definition and populate it.
    envelope_definition=EnvelopeDefinition(
        email_subject="Please sign this document sent from the Python SDK",
        # The Recipients object wants arrays for each recipient type
        template_id=session["template_id"],
        template_roles=[signer, cc],
        custom_fields=cf,
        status = "sent" # requests that the envelope be created and sent.
    )

    return envelope_definition
# ***DS.snippet.0.end

def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg017_set_template_tab_values.html",
                               title="SetTemplateTabValues",
                               template_ok="template_id" in session,
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
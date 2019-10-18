"""Example 013: Embedded Signing Ceremony from template with added document"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
from app import app, ds_config, views
import base64
import re
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg013"  # reference (and url) for this example
signer_client_id = 1000 # The id of the signer within this application.


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
    1. Check the token and presence of a saved template_id
    2. Call the worker method
    """
    minimum_buffer_min = 3
    token_ok = views.ds_token_ok(minimum_buffer_min)
    if token_ok and "template_id" in session:
        # 2. Call the worker method
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        pattern = re.compile("([^\w \-\@\.\,])+")
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name  = pattern.sub("", request.form.get("signer_name"))
        cc_email     = pattern.sub("", request.form.get("cc_email"))
        cc_name      = pattern.sub("", request.form.get("cc_name"))
        item         = pattern.sub("", request.form.get("item"))
        quantity     = pattern.sub("", request.form.get("quantity"))
        quantity     = int(quantity)
        template_id = session["template_id"]
        envelope_args = {
            "signer_email": signer_email,
            "signer_name": signer_name,
            "cc_email": cc_email,
            "cc_name": cc_name,
            "template_id": template_id,
            "signer_client_id": signer_client_id,
            "item": item,
            "quantity": quantity,
            "ds_return_url": url_for("ds_return", _external=True)
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
            # we can pull the DocuSign error code and message from the
            # response body
            error_body = json.loads(error_body_json)
            error_code = error_body and "errorCode" in error_body and \
                         error_body["errorCode"]
            error_message = error_body and "message" in error_body and \
                            error_body["message"]
            # In production, may want to provide customized error messages and
            # remediation advice to the user.
            return render_template("error.html",
                                   err=err,
                                   error_code=error_code,
                                   error_message=error_message
                                   )
        if results:
            # Redirect the user to the Signing Ceremony
            # Don't use an iFrame!
            # State can be stored/recovered using the framework's session
            return redirect(results["redirect_url"])

    elif not token_ok:
        flash("Sorry, you need to re-authenticate.")
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we"ll make the user re-enter the form data after
        # authentication.
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))
    elif not "template_id" in session:
        return render_template("eg013_add_doc_to_template.html",
            title="Embedded Signing Ceremony from template and extra doc",
            template_ok=False,
            source_file=path.basename(__file__),
            source_url=ds_config.DS_CONFIG["github_example_url"] +
                       path.basename(__file__),
            documentation=ds_config.DS_CONFIG["documentation"] + eg,
            show_doc=ds_config.DS_CONFIG["documentation"],
            )


# ***DS.snippet.0.start
def worker(args):
    """
    Create the envelope and the embedded Signing Ceremony
    1. Create the envelope request object using composite template to
       add the new document
    2. Send the envelope
    3. Make the recipient view request object
    4. Get the recipient view (Signing Ceremony) url
    """
    envelope_args = args["envelope_args"]
    # 1. Create the envelope request object
    envelope_definition = make_envelope(envelope_args)

    # 2. call Envelopes::create API method
    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args["base_path"]
    api_client.set_default_header("Authorization",
                                  "Bearer " + args["ds_access_token"])
    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(args["account_id"],
                                envelope_definition=envelope_definition)
    envelope_id = results.envelope_id

    # 3. Create the Recipient View request object
    authentication_method = "None"  # How is this application authenticating
    # the signer? See the "authenticationMethod" definition
    # https://goo.gl/qUhGTm
    recipient_view_request = RecipientViewRequest(
        authentication_method=authentication_method,
        client_user_id=envelope_args["signer_client_id"],
        recipient_id="1",
        return_url=envelope_args["ds_return_url"],
        user_name=envelope_args["signer_name"],
        email=envelope_args["signer_email"]
    )
    # 4. Obtain the recipient_view_url for the signing ceremony
    # Exceptions will be caught by the calling function
    results = envelope_api.create_recipient_view(args["account_id"],
                envelope_id,
                recipient_view_request=recipient_view_request)

    return {"envelope_id": envelope_id, "redirect_url": results.url}


def make_envelope(args):
    """
    Creates envelope
    Uses compositing templates to add a new document to the existing template
    returns an envelope definition

    The envelope request object uses Composite Template to
    include in the envelope:
    1. A template stored on the DocuSign service
    2. An additional document which is a custom HTML source document
    """

    # 1. Create Recipients for server template. Note that Recipients object
    #    is used, not TemplateRole
    #
    # Create a signer recipient for the signer role of the server template
    signer1 = Signer(email=args["signer_email"], name=args["signer_name"],
                     role_name="signer", recipient_id="1",
                     # Adding clientUserId transforms the template recipient
                     # into an embedded recipient:
                     client_user_id=args["signer_client_id"]
              )
    # Create the cc recipient
    cc1 = CarbonCopy(email=args["cc_email"], name=args["cc_name"],
                     role_name="cc", recipient_id="2"
                    )
    # Recipients object:
    recipients_server_template = Recipients(
        carbon_copies=[cc1], signers=[signer1])

    # 2. create a composite template for the Server template + roles
    comp_template1 = CompositeTemplate(
          composite_template_id="1",
          server_templates=[
              ServerTemplate(sequence="1", template_id=args["template_id"])
          ],
          # Add the roles via an inlineTemplate
          inline_templates=[
              InlineTemplate(sequence="1",
                             recipients=recipients_server_template)
          ]
    )

    # Next, create the second composite template that will
    # include the new document.
    #
    # 3. Create the signer recipient for the added document
    #    starting with the tab definition:
    sign_here1 = SignHere(anchor_string="**signature_1**",
                    anchor_y_offset="10", anchor_units="pixels",
                    anchor_x_offset="20")
    signer1_tabs = Tabs(sign_here_tabs=[sign_here1])

    # 4. Create Signer definition for the added document
    signer1AddedDoc = Signer(email=args["signer_email"],
                     name=args["signer_name"],
                     role_name="signer", recipient_id="1",
                     client_user_id=args["signer_client_id"],
                     tabs=signer1_tabs)
    # 5. The Recipients object for the added document.
    #    Using cc1 definition from above.
    recipients_added_doc = Recipients(
        carbon_copies=[cc1], signers=[signer1AddedDoc])
    # 6. Create the HTML document that will be added to the envelope
    doc1_b64 = base64.b64encode(bytes(create_document1(args), "utf-8"))\
               .decode("ascii")
    doc1 = Document(document_base64=doc1_b64,
            name="Appendix 1--Sales order", # can be different from
                                            # actual file name
            file_extension="html", document_id="1"
    )
    # 6. create a composite template for the added document
    comp_template2 = CompositeTemplate(composite_template_id="2",
        # Add the recipients via an inlineTemplate
        inline_templates=[
            InlineTemplate(sequence="2", recipients=recipients_added_doc)
        ],
        document=doc1
    )
    # 7. create the envelope definition with the composited templates
    envelope_definition = EnvelopeDefinition(
                            status="sent",
                            composite_templates=[comp_template1, comp_template2]
    )

    return envelope_definition


def create_document1(args):
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
          <meta charset="UTF-8">
        </head>
        <body style="font-family:sans-serif;margin-left:2em;">
        <h1 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
            color: darkblue;margin-bottom: 0;">World Wide Corp</h1>
        <h2 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
          margin-top: 0px;margin-bottom: 3.5em;font-size: 1em;
          color: darkblue;">Order Processing Division</h2>
        <h4>Ordered by {args["signer_name"]}</h4>
        <p style="margin-top:0em; margin-bottom:0em;">Email: {args["signer_email"]}</p>
        <p style="margin-top:0em; margin-bottom:0em;">Copy to: {args["cc_name"]}, {args["cc_email"]}</p>
        <p style="margin-top:3em; margin-bottom:0em;">Item: <b>{args["item"]}</b>, quantity: <b>{args["quantity"]}</b> at market price.</p>
        <p style="margin-top:3em;">
  Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. Donut jujubes oat cake jelly-o. Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
        </p>
        <!-- Note the anchor tag for the signature field is in white. -->
        <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
        </body>
    </html>
  """
# ***DS.snippet.0.end

def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg013_add_doc_to_template.html",
                               title="Embedded Signing Ceremony from template and extra doc",
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

"""Example 025: Applying a brand to an envelope"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views
import base64
import json
import re
from docusign_esign import ApiClient, EnvelopesApi, Document, Signer, SignHere, EnvelopeDefinition, Tabs, Recipients, \
                            AccountsApi
from docusign_esign.client.api_exception import ApiException

eg = 'eg025'    # reference and url for this example
demo_docs_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), "static/demo_documents"))
doc_file = "World_Wide_Corp_lorem.pdf"


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
    3. Render response
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):

        # More data validation would be a good idea here
        # Strip anything other than the characters listed
        pattern = re.compile("([^\w \-\@\.\,])+")
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))

        # Step 1: Obtain your OAuth token
        args = {
            'account_id': session['ds_account_id'],  # represent your {ACCOUNT_ID}
            'base_path': session['ds_base_path'],
            'access_token': session['ds_access_token'],   # represent your {ACCESS_TOKEN}
            'envelope_args': {
                'signer_name': signer_name,
                'signer_email': signer_email,
                'brand_id': request.form.get('brand')
            }

        }
        try:
            # Step 2: Call the worker method to apply brand to the envelope
            response = worker(args)
            envelope_id = response.envelope_id
            app.logger.info(f"Brand has been applied to envelope. Envelope id {envelope_id}")

            # Step 3: Render a response
            return render_template('example_done.html',
                                   title='Brand applying to envelope',
                                   h1='Brand applying to envelope',
                                   message=f"""The brand has been applied to envelope!<br/>
                                               Envelope ID: {envelope_id}."""
            )

        except ApiException as err:
            error_body_json = err and hasattr(err, 'body') and err.body
            # We can pull the DocuSign error code and message from the response body
            error_body = json.loads(error_body_json)
            error_code = error_body and 'errorCode' in error_body and error_body['errorCode']
            error_message = error_body and "message" in error_body and error_body["message"]
            # In production, you may want to provide customized error messages and
            # remediation advice to the user
            return render_template('error.html',
                                   err=err,
                                   error_code=error_code,
                                   error_message=error_message
                                   )

    else:
        flash("Sorry, you need to re-authenticate.")
        # We could store the parameters of the requested operation so it could be restarted
        # automatically. But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


def worker(args):
    """
    1. Call create_api_client method
    2. Call make_envelope method
    3. Apply the brand to the envelope using SDK
    """

    # Step 1: Call create_api_client method
    api_client = create_api_client(args)

    # Step 2: Call make_envelope method
    envelope_api = EnvelopesApi(api_client)
    envelope_definition = make_envelope(args['envelope_args'])

    # Step 3: Apply the brand to the envelope using SDK
    response = envelope_api.create_envelope(args['account_id'], envelope_definition=envelope_definition)

    return response


def create_api_client(args):
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {args['access_token']}")

    return api_client


def make_envelope(args):
    """
    Creates envelope
    """

    # Open example file
    with open(path.join(demo_docs_path, doc_file), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode("ascii")

    document = Document(
        document_base64=base64_file_content,
        name='lorem',
        file_extension='pdf',
        document_id=1
    )

    signer = Signer(
        email=args['signer_email'],
        name=args['signer_name'],
        recipient_id="1",
        routing_order="1"
    )

    sign_here = SignHere(
        anchor_string='/sn1/',
        anchor_units='pixels',
        anchor_y_offset="572",
        anchor_x_offset="75"
    )

    signer.tabs = Tabs(sign_here_tabs=[sign_here])

    envelope_definition = EnvelopeDefinition(
        email_subject='Please Sign',
        documents=[document],
        recipients=Recipients(signers=[signer]),
        status='sent',
        brand_id=args['brand_id'],
    )

    return envelope_definition


def get_brands():
    """Retrieve all brands using the AccountBrands::List"""
    args = {
        'account_id': session['ds_account_id'],  # represent your {ACCOUNT_ID}
        'base_path': session['ds_base_path'],
        'access_token': session['ds_access_token'],  # represent your {ACCESS_TOKEN}

    }
    api_client = create_api_client(args)
    try:
        account_api = AccountsApi(api_client)
        response = account_api.list_brands(args['account_id'])
        return response.brands
    except ApiException as err:
        error_body_json = err and hasattr(err, 'body') and err.body
        # We can pull the DocuSign error code and message from the response body
        error_body = json.loads(error_body_json)
        error_code = error_body and 'errorCode' in error_body and error_body['errorCode']
        error_message = error_body and "message" in error_body and error_body["message"]
        # In production, you may want to provide customized error messages and
        # remediation advice to the user
        return render_template('error.html',
                               err=err,
                               error_code=error_code,
                               error_message=error_message
                               )


def get_controller():
    """Responds with the form for the example"""
    if views.ds_token_ok():
        # Get all brands to render it in the template
        brands = get_brands()

        return render_template("eg025_brands_apply_to_envelope.html",
                               title="Applying a brand to a template",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               brands=brands,
                               signer_name=ds_config.DS_CONFIG["signer_name"],
                               signer_email=ds_config.DS_CONFIG["signer_email"]
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))

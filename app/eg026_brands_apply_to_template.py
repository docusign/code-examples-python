"""Example 026: Applying a brand to a template"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views
import json
import re
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, TemplateRole, AccountsApi, TemplatesApi
from docusign_esign.client.api_exception import ApiException

eg = 'eg026'    # reference and url for this example


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
    3. Render a response
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):

        # More data validation would be a good idea here
        # Strip anything other than the characters listed
        pattern = re.compile("([^\w \-\@\.\,])+")
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = request.form.get('cc_email')
        cc_name = request.form.get('cc_name')

        if cc_email and cc_name:
            cc_email = pattern.sub("", cc_email)
            cc_name = pattern.sub("", cc_name)

        # Step 1: Obtain your OAuth token
        args = {
            'account_id': session['ds_account_id'],  # represent your {ACCOUNT_ID}
            'base_path': session['ds_base_path'],
            'access_token': session['ds_access_token'],   # represent your {ACCESS_TOKEN}
            'envelope_args': {
                'signer_name': signer_name,
                'signer_email': signer_email,
                'cc_name': cc_name,
                'cc_email': cc_email,
                'brand_id': request.form.get('brand'),
                'template_id': request.form.get('envelope_template')
            }
        }
        try:
            # Step 2: Call the worker method to apply the brand to the template
            response = worker(args)
            envelope_id = response.envelope_id
            app.logger.info(f"Brand has been applied to envelope. Envelope id {envelope_id}")

            return render_template('example_done.html',
                                   title='Brand applying to template',
                                   h1='Brand applying to template',
                                   message=f"""The brand has been applied to template!<br/>
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

    # Step 2: Call make_envelope method to create an envelope definition with Signer
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
    args -- parameters for the envelope:
    signer_email, signer_name, signer_client_id
    returns an envelope definition
    """
    # Create the envelope definition
    envelope_definition = EnvelopeDefinition(
        status='sent',
        template_id=args['template_id'],
        brand_id=args['brand_id']
        )

    signer = TemplateRole(
        email=args['signer_email'],
        name=args['signer_name'],
        role_name='signer'
        )

    # In case, we have cc we add him to envelope definition
    if args['cc_email'] and args['cc_name']:
        cc = TemplateRole(
            email=args['cc_email'],
            name=args['cc_name'],
            role_name='cc'
        )

        envelope_definition.template_roles = [signer, cc]

    else:
        envelope_definition.template_roles = [signer]

    return envelope_definition


def get_data():
    """Retrieve brands and envelope templates"""
    args = {
        'account_id': session['ds_account_id'],  # represent your {ACCOUNT_ID}
        'base_path': session['ds_base_path'],
        'access_token': session['ds_access_token'],  # represent your {ACCESS_TOKEN}
    }
    api_client = create_api_client(args)

    try:
        """Retrieve all brands using the AccountBrands::List"""
        account_api = AccountsApi(api_client)
        brands = account_api.list_brands(args['account_id']).brands

        """Retrieve all templates using the Templates::List"""
        template_api = TemplatesApi(api_client)
        envelope_templates = template_api.list_templates(args['account_id']).envelope_templates

        return brands, envelope_templates

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
        brands, templates = get_data()
        return render_template("eg026_brands_apply_to_template.html",
                               title="Applying a brand to a template",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               brands=brands,
                               templates=templates,
                               signer_name=ds_config.DS_CONFIG["signer_name"],
                               signer_email=ds_config.DS_CONFIG["signer_email"],
                            )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))






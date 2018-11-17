"""Example 009: Send envelope using a template"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
from app import app, ds_config, views
import base64
import re
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg009"  # reference (and url) for this example


def controller():
    """Controller router using the HTTP method"""
    if request.method == 'GET':
        return get_controller()
    elif request.method == 'POST':
        return create_controller()
    else:
        return render_template('404.html'), 404


def create_controller():
    """
    1. Check the token
    2. Call the worker method
    """
    minimum_buffer_min = 3
    token_ok = views.ds_token_ok(minimum_buffer_min)
    if token_ok and 'template_id' in session:
        # 2. Call the worker method
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        pattern = re.compile('([^\w \-\@\.\,])+')
        signer_email = pattern.sub('', request.form.get('signer_email'))
        signer_name  = pattern.sub('', request.form.get('signer_name'))
        cc_email     = pattern.sub('', request.form.get('cc_email'))
        cc_name      = pattern.sub('', request.form.get('cc_name'))
        envelope_args = {
            'signer_email': signer_email,
            'signer_name': signer_name,
            'cc_email': cc_email,
            'cc_name': cc_name,
            'template_id': template_id
        }
        args = {
            'account_id': session['ds_account_id'],
            'base_path': session['ds_base_path'],
            'ds_access_token': session['ds_access_token'],
            'envelope_args': envelope_args
        }

        try:
            results = worker(args)
        except ApiException as err:
            error_body_json = err and hasattr(err, 'body') and err.body
            # we can pull the DocuSign error code and message from the response body
            error_body = json.loads(error_body_json)
            error_code = error_body and 'errorCode' in error_body and error_body['errorCode']
            error_message = error_body and 'message' in error_body and error_body['message']
            # In production, may want to provide customized error messages and
            # remediation advice to the user.
            return render_template('error.html',
                                   err=err,
                                   error_code=error_code,
                                   error_message=error_message
                                   )
        if results:
            return render_template('example_done.html',
                        title="Envelope sent",
                        h1="Envelope sent",
                        message=f"""The envelope has been created and sent!<br/>
                        Envelope ID {results["envelope_id"]}."""
            )
    elsif not token_ok:
        flash('Sorry, you need to re-authenticate.')
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after
        # authentication.
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))
    elif not 'template_id' in session:
        return render_template("eg009_use_template.html",
                               title="Use a template to send an envelope",
                               template_ok=False,
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG['github_example_url'] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG['documentation'] + eg,
                               show_doc=ds_config.DS_CONFIG['documentation'],
                               )


def worker(args):
    """
    1. Create the envelope request object
    2. Send the envelope
    """
    envelope_args = args["envelope_args"]
    # 1. Create the envelope request object
    envelope_definition = make_envelope(envelope_args)

    # 2. call Envelopes::create API method
    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header("Authorization", "Bearer " + args['ds_access_token'])
    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(args['account_id'], envelope_definition=envelope_definition)
    envelope_id = results.envelope_id
    return {'envelope_id': envelope_id}

# ***DS.worker.end ***DS.snippet.1.end


# ***DS.snippet.2.start
def make_envelope(args):
    """
    Creates envelope
    args -- parameters for the envelope:
    signer_email, signer_name, signer_client_id
    returns an envelope definition
    """

    # create the envelope definition
    envelope_definition = EnvelopeDefinition(
        status = "sent" # requests that the envelope be created and sent.
        templateId = args['template_id']
    )
    # Create template role elements to connect the signer and cc recipients
    # to the template
    signer = TemplateRole(
        email = args['signer_email'],
        name = args['signer_name'],
        role_name = 'signer')
    // Create a cc template role.
    cc = TemplateRole(
        email = args['cc_email'],
        name = args['cc_name'],
        role_name = 'cc')

    # Add the TemplateRole objects to the envelope object
    envelope_definition.template_roles = [signer, cc]
    return envelope_definition

# ***DS.snippet.2.end
def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg009_use_template.html",
                               title="Use a template to send an envelope",
                               template_ok="template_id" in session,
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG['github_example_url'] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG['documentation'] + eg,
                               show_doc=ds_config.DS_CONFIG['documentation'],
                               signer_name=ds_config.DS_CONFIG['signer_name'],
                               signer_email=ds_config.DS_CONFIG['signer_email']
        )
    else:
        # Save the current operation so it will be resumed after authentication
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))

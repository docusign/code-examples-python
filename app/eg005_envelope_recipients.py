"""005: List an envelope's recipients and status

Also, for issue 22, lists tabs for the signer recipient.
See https://github.com/docusign/docusign-python-client/issues/22
"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
from app import ds_config, views
from docusign_esign import *
from docusign_esign.client.api_exception import ApiException

eg = "eg005"  # reference (and url) for this example

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
    3. Show results
    """
    minimum_buffer_min = 3
    token_ok = views.ds_token_ok(minimum_buffer_min)
    if token_ok and 'envelope_id' in session:
        # 2. Call the worker method
        args = {
            'account_id': session['ds_account_id'],
            'envelope_id': session['envelope_id'],
            'base_path': session['ds_base_path'],
            'ds_access_token': session['ds_access_token'],
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
        return render_template("example_done.html",
                                title="Envelope recipients results",
                                h1="List the envelope's recipients and their status",
                                message="Results from the EnvelopeRecipientTabs::list method. API method: envelope_api.list_tabs",
                                json=json.dumps(json.dumps(results.to_dict()))
                                )
    elif not token_ok:
        flash('Sorry, you need to re-authenticate.')
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after
        # authentication.
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))
    elif not 'envelope_id' in session:
        return render_template("eg005_envelope_recipients.html",
                               title="Envelope recipient information",
                               envelope_ok=False,
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG['github_example_url'] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG['documentation'] + eg,
                               show_doc=ds_config.DS_CONFIG['documentation'],
                               )


# ***DS.snippet.0.start
def worker(args):
    """
    1. Call the envelope recipients list method
    """

    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header("Authorization", "Bearer " + args['ds_access_token'])
    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.list_recipients(args['account_id'], args['envelope_id'])

    recipientId = results.signers[0].recipient_id
    # Call the EnvelopeRecipientTabs: list method
    envelope_api = EnvelopesApi(api_client)
    results2 = envelope_api.list_tabs(args['account_id'], args['envelope_id'], recipientId)

    return results2
# ***DS.snippet.0.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg005_envelope_recipients.html",
                               title="Envelope recipient information",
                               envelope_ok='envelope_id' in session,
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG['github_example_url'] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG['documentation'] + eg,
                               show_doc=ds_config.DS_CONFIG['documentation'],
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))


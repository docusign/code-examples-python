"""012: Embedded console"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
import re
from app import ds_config, views
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg012"  # reference (and url) for this example

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
    if token_ok:
        # 2. Call the worker method
        # Strip anything other than characters listed
        pattern = re.compile('([^\w \-\@\.\,])+')
        starting_view = pattern.sub('', request.form.get('starting_view'))
        envelope_id = 'envelope_id' in session and session['envelope_id']
        args = {
            'envelope_id': envelope_id,
            'starting_view': starting_view,
            'account_id': session['ds_account_id'],
            'base_path': session['ds_base_path'],
            'ds_access_token': session['ds_access_token'],
            'ds_return_url': url_for('ds_return', _external=True),
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
            # Redirect the user to the NDSE view
            # Don't use an iFrame!
            # State can be stored/recovered using the framework's session
            return redirect(results["redirect_url"])

    else:
        flash('Sorry, you need to re-authenticate.')
        # We could store the parameters of the requested operation
        # so it could be restarted automatically.
        # But since it should be rare to have a token issue here,
        # we'll make the user re-enter the form data after
        # authentication.
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))


# ***DS.snippet.0.start
def worker(args):
    """
    This function does the work of returning a URL for the NDSE view
    """

    # Step 1. Create the NDSE view request object
    # Set the url where you want the recipient to go once they are done
    # with the NDSE. It is usually the case that the
    # user will never "finish" with the NDSE.
    # Assume that control will not be passed back to your app.
    view_request = ConsoleViewRequest(return_url=args['ds_return_url'])
    if args['starting_view'] == "envelope" and args['envelope_id']:
        view_request.envelope_id = args['envelope_id']

    # Step 2. Get the console view url
    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header("Authorization", "Bearer " + args['ds_access_token'])
    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_console_view(args['account_id'], console_view_request=view_request)
    url = results.url
    return {'redirect_url': url}
# ***DS.snippet.0.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        envelope_id = 'envelope_id' in session and session['envelope_id']
        return render_template("eg012_embedded_console.html",
                               title="Embedded Console",
                               envelope_ok=envelope_id,
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG['github_example_url'] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG['documentation'] + eg,
                               show_doc=ds_config.DS_CONFIG['documentation'],
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))


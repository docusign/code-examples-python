"""Example 001: Embedded Signing Ceremony"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
from app import app, ds_config, views
import base64
import re
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg001"  # reference (and url) for this example
signer_client_id = 1000 # Used to indicate that the signer will use an embedded
                        # Signing Ceremony. Represents the signer's userId within
                        # your application.
authentication_method = 'None' # How is this application authenticating
                               # the signer? See the `authenticationMethod' definition
                               # https://developers.docusign.com/esign-rest-api/reference/Envelopes/EnvelopeViews/createRecipient

demo_docs_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), 'static/demo_documents'))


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
    3. Redirect the user to the signing ceremony
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):
        # 2. Call the worker method
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        pattern = re.compile('([^\w \-\@\.\,])+')
        signer_email = pattern.sub('', request.form.get('signer_email'))
        signer_name  = pattern.sub('', request.form.get('signer_name'))
        envelope_args = {
            'signer_email': signer_email,
            'signer_name': signer_name,
            'signer_client_id': signer_client_id,
            'ds_return_url': url_for('ds_return', _external=True),
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
            # Redirect the user to the Signing Ceremony
            # Don't use an iFrame!
            # State can be stored/recovered using the framework's session or a
            # query parameter on the returnUrl (see the makeRecipientViewRequest method)
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
    api_client.host = args['base_path']
    api_client.set_default_header("Authorization", "Bearer " + args['ds_access_token'])

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(args['account_id'], envelope_definition=envelope_definition)
    
    envelope_id = results.envelope_id
    app.logger.info(f'Envelope was created. EnvelopeId {envelope_id}')

    # 3. Create the Recipient View request object
    recipient_view_request = RecipientViewRequest(
        authentication_method = authentication_method,
        client_user_id = envelope_args['signer_client_id'],
        recipient_id = '1',
        return_url = envelope_args['ds_return_url'],
        user_name = envelope_args['signer_name'], email = envelope_args['signer_email']
    )
    # 4. Obtain the recipient_view_url for the signing ceremony
    # Exceptions will be caught by the calling function
    results = envelope_api.create_recipient_view(args['account_id'], envelope_id,
        recipient_view_request = recipient_view_request)

    return {'envelope_id': envelope_id, 'redirect_url': results.url}

# ***DS.worker.end ***DS.snippet.1.end


# ***DS.snippet.2.start
def make_envelope(args):
    """
    Creates envelope
    args -- parameters for the envelope:
    signer_email, signer_name, signer_client_id
    returns an envelope definition
    """

    # document 1 (pdf) has tag /sn1/
    #
    # The envelope has one recipient.
    # recipient 1 - signer
    with open(path.join(demo_docs_path, ds_config.DS_CONFIG['doc_pdf']), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    # Create the document model
    document = Document( # create the DocuSign document object
        document_base64 = base64_file_content,
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model
    signer = Signer( # The signer
        email = args['signer_email'], name = args['signer_name'],
        recipient_id = "1", routing_order = "1",
        # Setting the client_user_id marks the signer as embedded
        client_user_id = args['signer_client_id']
    )

    # Create a sign_here tab (field on the document)
    sign_here = SignHere( # DocuSign SignHere field/tab
        anchor_string = '/sn1/', anchor_units = 'pixels',
        anchor_y_offset = '10', anchor_x_offset = '20'
    )

    # Add the tabs model (including the sign_here tab) to the signer
    # The Tabs object wants arrays of the different field/tab types
    signer.tabs = Tabs(sign_here_tabs = [sign_here])

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this document sent from the Python SDK",
        documents = [document],
        # The Recipients object wants arrays for each recipient type
        recipients = Recipients(signers = [signer]),
        status = "sent" # requests that the envelope be created and sent.
    )

    return envelope_definition


# ***DS.snippet.2.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg001_embedded_signing.html",
                               title="Embedded Signing Ceremony",
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


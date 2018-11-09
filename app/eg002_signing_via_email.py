""" Example 002: Remote signer, cc, envelope has three documents """

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views
import base64
import re
import json
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg002"  # reference (and url) for this example
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
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):
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
            'status': 'sent',
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
            session["envelope_id"] = results["envelope_id"] # Save for use by other examples
                                                            # which need an envelopeId
            return render_template('example_done.html',
                        title="Envelope sent",
                        h1="Envelope sent",
                        message=f"""The envelope has been created and sent!<br/>
                        Envelope ID {results["envelope_id"]}."""
            )

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

    return {'envelope_id': envelope_id}


# ***DS.worker.end ***DS.snippet.1.end


# ***DS.snippet.2.start
def make_envelope(args):
    """
    Creates envelope
    Document 1: An HTML document.
    Document 2: A Word .docx document.
    Document 3: A PDF document.
    DocuSign will convert all of the documents to the PDF format.
    The recipients' field tags are placed using <b>anchor</b> strings.
    """

    # document 1 (html) has sign here anchor tag **signature_1**
    # document 2 (docx) has sign here anchor tag /sn1/
    # document 3 (pdf)  has sign here anchor tag /sn1/
    #
    # The envelope has two recipients.
    # recipient 1 - signer
    # recipient 2 - cc
    # The envelope will be sent first to the signer.
    # After it is signed, a copy is sent to the cc person.

    # create the envelope definition
    env = EnvelopeDefinition(
        email_subject='Please sign this document set'
    )
    doc1_b64 = base64.b64encode(bytes(create_document1(args), 'utf-8')).decode('ascii')
    # read files 2 and 3 from a local directory
    # The reads could raise an exception if the file is not available!
    with open(path.join(demo_docs_path, ds_config.DS_CONFIG['doc_docx']), "rb") as file:
        doc2_docx_bytes = file.read()
    doc2_b64 = base64.b64encode(doc2_docx_bytes).decode('ascii')
    with open(path.join(demo_docs_path, ds_config.DS_CONFIG['doc_pdf']), "rb") as file:
        doc3_pdf_bytes = file.read()
    doc3_b64 = base64.b64encode(doc3_pdf_bytes).decode('ascii')

    # Create the document models
    document1 = Document(  # create the DocuSign document object
        document_base64=doc1_b64,
        name='Order acknowledgement',  # can be different from actual file name
        file_extension='html',  # many different document types are accepted
        document_id='1'  # a label used to reference the doc
    )
    document2 = Document(  # create the DocuSign document object
        document_base64=doc2_b64,
        name='Battle Plan',  # can be different from actual file name
        file_extension='docx',  # many different document types are accepted
        document_id='2'  # a label used to reference the doc
    )
    document3 = Document(  # create the DocuSign document object
        document_base64=doc3_b64,
        name='Lorem Ipsum',  # can be different from actual file name
        file_extension='pdf',  # many different document types are accepted
        document_id='3'  # a label used to reference the doc
    )
    # The order in the docs array determines the order in the envelope
    env.documents = [document1, document2, document3]


    # Create the signer recipient model
    signer1 = Signer(
        email=args['signer_email'], name=args['signer_name'],
        recipient_id="1", routing_order="1"
    )
    # routingOrder (lower means earlier) determines the order of deliveries
    # to the recipients. Parallel routing order is supported by using the
    # same integer as the order for two or more recipients.

    # create a cc recipient to receive a copy of the documents
    cc1 = CarbonCopy(
        email=args['cc_email'], name=args['cc_name'],
        recipient_id="2", routing_order="2")

    # Create signHere fields (also known as tabs) on the documents,
    # We're using anchor (autoPlace) positioning
    #
    # The DocuSign platform searches throughout your envelope's
    # documents for matching anchor strings. So the
    # signHere2 tab will be used in both document 2 and 3 since they
    #  use the same anchor string for their "signer 1" tabs.
    sign_here1 = SignHere(
        anchor_string = '**signature_1**', anchor_units = 'pixels',
        anchor_y_offset = '10', anchor_x_offset = '20')
    sign_here2 = SignHere(
        anchor_string = '/sn1/', anchor_units = 'pixels',
        anchor_y_offset = '10', anchor_x_offset = '20')

    # Add the tabs model (including the sign_here tabs) to the signer
    # The Tabs object wants arrays of the different field/tab types
    signer1.tabs = Tabs(sign_here_tabs=[sign_here1, sign_here2])

    # Add the recipients to the envelope object
    recipients = Recipients(signers=[signer1], carbon_copies=[cc1])
    env.recipients = recipients

    # Request that the envelope be sent by setting |status| to "sent".
    # To request that the envelope be created as a draft, set to "created"
    env.status = args["status"]

    return env


# ***DS.snippet.3.start
def create_document1(args):
    """ Creates document 1 -- an html document"""

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
          <meta charset="UTF-8">
        </head>
        <body style="font-family:sans-serif;margin-left:2em;">
        <h1 style="font-family: 'Trebuchet MS', Helvetica, sans-serif;
            color: darkblue;margin-bottom: 0;">World Wide Corp</h1>
        <h2 style="font-family: 'Trebuchet MS', Helvetica, sans-serif;
          margin-top: 0px;margin-bottom: 3.5em;font-size: 1em;
          color: darkblue;">Order Processing Division</h2>
        <h4>Ordered by {args['signer_name']}</h4>
        <p style="margin-top:0em; margin-bottom:0em;">Email: {args['signer_email']}</p>
        <p style="margin-top:0em; margin-bottom:0em;">Copy to: {args['cc_name']}, {args['cc_email']}</p>
        <p style="margin-top:3em;">
  Candy bonbon pastry jujubes lollipop wafer biscuit biscuit. Topping brownie sesame snaps sweet roll pie. Croissant danish biscuit soufflé caramels jujubes jelly. Dragée danish caramels lemon drops dragée. Gummi bears cupcake biscuit tiramisu sugar plum pastry. Dragée gummies applicake pudding liquorice. Donut jujubes oat cake jelly-o. Dessert bear claw chocolate cake gummies lollipop sugar plum ice cream gummies cheesecake.
        </p>
        <!-- Note the anchor tag for the signature field is in white. -->
        <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
        </body>
    </html>
  """
  # ***DS.snippet.3.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg002_signing_via_email.html",
                               title="Signing via email",
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



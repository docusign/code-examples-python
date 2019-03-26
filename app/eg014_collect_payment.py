""" Example 014: Remote signer, cc; envelope has an order form """

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views
import base64
import re
import json
from docusign_esign import *
from docusign_esign.client.api_exception import ApiException

eg = "eg014"  # reference (and url) for this example
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
            'gateway_account_id': ds_config.DS_CONFIG['gateway_account_id'],
            'gateway_name': ds_config.DS_CONFIG['gateway_name'],
            'gateway_display_name': ds_config.DS_CONFIG['gateway_display_name']
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
    # app.logger.info(f'Envelope was created. EnvelopeId {envelope_id}')

    return {'envelope_id': envelope_id}


# ***DS.worker.end ***DS.snippet.1.end


# ***DS.snippet.2.start
def make_envelope(args):
    """
    This function creates the envelope definition for the
    order form.
    document 1 (html) has multiple tags:
     /l1q/ and /l2q/ -- quantities: drop down
     /l1e/ and /l2e/ -- extended: payment lines
     /l3t/ -- total -- formula

    The envelope has two recipients.
      recipient 1 - signer
      recipient 2 - cc
    The envelope will be sent first to the signer.
    After it is signed, a copy is sent to the cc person.

    #################################################################
    #                                                               #
    # NOTA BENA: This method programmatically constructs the        #
    #            order form. For many use cases, it would be        #
    #            better to create the order form as a template      #
    #            using the DocuSign web tool as WYSIWYG             #
    #            form designer.                                     #
    #                                                               #
    #################################################################

    """

    # Order form constants
    l1_name = "Harmonica"
    l1_price = 5
    l1_description = f"${l1_price} each"
    l2_name = "Xylophone"
    l2_price = 150
    l2_description = f"${l2_price} each"
    currency_multiplier = 100

    # read the html file from a local directory
    # The read could raise an exception if the file is not available!
    doc1_file = 'order_form.html'
    with open(path.join(demo_docs_path, doc1_file), "r") as file:
        doc1_html_v1 = file.read()

    # Substitute values into the HTML
    # Substitute for: {signerName}, {signerEmail}, {cc_name}, {cc_email}
    doc1_html_v2 = doc1_html_v1.replace('{signer_name}', args['signer_name']) \
                        .replace('{signer_email}', args['signer_email'])      \
                        .replace('{cc_name}', args['cc_name'])               \
                        .replace('{cc_email}', args['cc_email'])

    # create the envelope definition
    envelope_definition = EnvelopeDefinition(
                            email_subject='Please complete your order')
    # add the document
    doc1_b64 = base64.b64encode(bytes(doc1_html_v2, 'utf-8')).decode('ascii')
    doc1 = Document(document_base64=doc1_b64,
                    name='Order form', # can be different from actual file name
                    file_extension='html', # Source data format.
                    document_id='1' # a label used to reference the doc
                    )
    envelope_definition.documents = [doc1]
    # create a signer recipient to sign the document
    signer1 = Signer(email=args['signer_email'], name=args['signer_name'],
                     recipient_id="1", routing_order="1")
    # create a cc recipient to receive a copy of the documents
    cc1 = CarbonCopy(email=args['cc_email'], name=args['cc_name'],
                     recipient_id="2", routing_order="2")
    # Create signHere fields (also known as tabs) on the documents,
    # We're using anchor (autoPlace) positioning
    sign_here1 = SignHere(
            anchor_string='/sn1/',
            anchor_y_offset='10', anchor_units='pixels',
            anchor_x_offset='20')
    list_item0 = ListItem(text="none", value="0")
    list_item1 = ListItem(text="1", value="1")
    list_item2 = ListItem(text="2", value="2")
    list_item3 = ListItem(text="3", value="3")
    list_item4 = ListItem(text="4", value="4")
    list_item5 = ListItem(text="5", value="5")
    list_item6 = ListItem(text="6", value="6")
    list_item7 = ListItem(text="7", value="7")
    list_item8 = ListItem(text="8", value="8")
    list_item9 = ListItem(text="9", value="9")
    list_item10 = ListItem(text="10", value="10")

    listl1q = List(
            font="helvetica",
            font_size="size11",
            anchor_string='/l1q/',
            anchor_y_offset='-10', anchor_units='pixels',
            anchor_x_offset='0',
            list_items=[list_item0, list_item1, list_item2,
                list_item3, list_item4, list_item5, list_item6,
                list_item7, list_item8, list_item9, list_item10],
            required="true",
            tab_label="l1q"
            )
    listl2q = List(
            font="helvetica",
            font_size="size11",
            anchor_string='/l2q/',
            anchor_y_offset='-10', anchor_units='pixels',
            anchor_x_offset='0',
            list_items=[list_item0, list_item1, list_item2,
                list_item3, list_item4, list_item5, list_item6,
                list_item7, list_item8, list_item9, list_item10],
            required="true",
            tab_label="l2q"
            )
    # create two formula tabs for the extended price on the line items
    formulal1e = FormulaTab(
            font="helvetica",
            font_size="size11",
            anchor_string='/l1e/',
            anchor_y_offset='-8', anchor_units='pixels',
            anchor_x_offset='105',
            tab_label="l1e",
            formula=f'[l1q] * {l1_price}',
            round_decimal_places="0",
            required="true",
            locked="true",
            disable_auto_size="false",
            )
    formulal2e = FormulaTab(
            font="helvetica",
            font_size="size11",
            anchor_string='/l2e/',
            anchor_y_offset='-8', anchor_units='pixels',
            anchor_x_offset='105',
            tab_label="l2e",
            formula=f'[l2q] * {l2_price}',
            round_decimal_places="0",
            required="true",
            locked="true",
            disable_auto_size="false",
            )
    # Formula for the total
    formulal3t = FormulaTab(
            font="helvetica",
            bold="true",
            font_size="size12",
            anchor_string='/l3t/',
            anchor_y_offset='-8', anchor_units='pixels',
            anchor_x_offset='50',
            tab_label="l3t",
            formula='[l1e] + [l2e]',
            round_decimal_places="0",
            required="true",
            locked="true",
            disable_auto_size="false",
            )
    # Payment line items
    payment_line_iteml1 = PaymentLineItem(
            name=l1_name, description=l1_description, amount_reference="l1e"
            )
    payment_line_iteml2 = PaymentLineItem(
            name=l2_name, description=l2_description, amount_reference="l2e"
            )
    payment_details = PaymentDetails(
            gateway_account_id=args['gateway_account_id'],
            currency_code="USD",
            gateway_name=args['gateway_name'],
            line_items=[payment_line_iteml1, payment_line_iteml2]
            )
    # Hidden formula for the payment itself
    formula_payment = FormulaTab(
            tab_label="payment",
            formula=f'([l1e] + [l2e]) * {currency_multiplier}',
            round_decimal_places="0",
            payment_details=payment_details,
            hidden="true",
            required="true",
            locked="true",
            document_id="1",
            page_number="1",
            x_position="0",
            y_position="0"
            )

    # Tabs are set per recipient / signer
    signer1_tabs = Tabs(
            sign_here_tabs=[sign_here1],
            list_tabs=[listl1q, listl2q],
            formula_tabs=[formulal1e, formulal2e, formulal3t, formula_payment]
        )
    signer1.tabs = signer1_tabs

    # Add the recipients to the envelope object
    recipients = Recipients(signers=[signer1], carbon_copies=[cc1]);
    envelope_definition.recipients = recipients

    # Request that the envelope be sent by setting |status| to "sent".
    # To request that the envelope be created as a draft, set to "created"
    envelope_definition.status = args['status']

    return envelope_definition
# ***DS.snippet.0.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        gateway = ds_config.DS_CONFIG['gateway_account_id']
        gateway_ok = gateway and len(gateway) > 25

        return render_template("eg014_collect_payment.html",
                               title="Order form with payment",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG['github_example_url'] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG['documentation'] + eg,
                               show_doc=ds_config.DS_CONFIG['documentation'],
                               signer_name=ds_config.DS_CONFIG['signer_name'],
                               signer_email=ds_config.DS_CONFIG['signer_email'],
                               gateway_ok=gateway_ok
        )
    else:
        # Save the current operation so it will be resumed after authentication
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))

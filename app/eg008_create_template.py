""" Example 008: create a template if it doesn't already exist """

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views
import base64
import re
import json
from docusign_esign import *
from docusign_esign.rest import ApiException

eg = "eg008"  # reference (and url) for this example
demo_docs_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), 'static/demo_documents'))
template_name = 'Example Signer and CC template'
doc_file = 'World_Wide_Corp_fields.pdf'


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
        args = {
            'account_id': session['ds_account_id'],
            'base_path': session['ds_base_path'],
            'ds_access_token': session['ds_access_token']
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
            # Save the templateId in the session so they can be used in future examples
            session['template_id'] = results['template_id']
            msg = "The template has been created!" if results['created_new_template'] else \
                  "Done. The template already existed in your account."
            return render_template('example_done.html',
                        title="Template results",
                        h1="Template results",
                        message=f"""{msg}<br/>Template name: {results['template_name']}, 
                        ID {results['template_id']}."""
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
    1. Check to see if the template already exists
    2. If not, create the template
    """
    # 1. call Templates::list API method
    # Exceptions will be caught by the calling function
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header("Authorization", "Bearer " + args['ds_access_token'])
    templates_api = TemplatesApi(api_client)
    results = templates_api.list_templates(args['account_id'], search_text=template_name)
    results_template_name = None
    created_new_template = False
    if int(results.result_set_size) > 0:
        template_id = results.envelope_templates[0].template_id
        results_template_name = results.envelope_templates[0].name
    else:
        # Template not found -- so create it
        # Step 2 create the template
        template_req_object = make_template_req()
        results = templates_api.create_template(args['account_id'], envelope_template=template_req_object)
        template_id = results.template_id
        results_template_name = results.name
        created_new_template = True
    return {
        'template_id': template_id,
        'template_name': results_template_name,
        'created_new_template': created_new_template}


def make_template_req():
    """Creates template req object"""

    # document 1 (pdf)
    #
    # The template has two recipient roles.
    # recipient 1 - signer
    # recipient 2 - cc
    with open(path.join(demo_docs_path, doc_file), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    # Create the document model
    document = Document( # create the DocuSign document object
        document_base64 = base64_file_content,
        name = 'Lorem Ipsum', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model
    signer = Signer(role_name='signer', recipient_id="1", routing_order="1")
    # create a cc recipient to receive a copy of the envelope (transaction)
    cc = CarbonCopy(role_name='cc', recipient_id="2", routing_order="2")
    # Create fields using absolute positioning
    # Create a sign_here tab (field on the document)
    sign_here = SignHere(document_id='1', page_number='1', x_position='191', y_position='148')
    check1 = Checkbox(document_id='1', page_number='1', x_position='75', y_position='417',
                      tab_label='ckAuthorization')
    check2 = Checkbox(document_id='1', page_number='1', x_position='75', y_position='447',
                      tab_label='ckAuthentication')
    check3 = Checkbox(document_id='1', page_number='1', x_position='75', y_position='478',
                      tab_label='ckAgreement')
    check4 = Checkbox(document_id='1', page_number='1', x_position='75', y_position='508',
                      tab_label='ckAcknowledgement')
    list1 = List(document_id="1", page_number="1", x_position="142", y_position="291",
            font="helvetica", font_size="size14", tab_label="list",
            required="false",
            list_items=[
                ListItem(text="Red"   , value="red"   ),
                ListItem(text="Orange", value="orange"),
                ListItem(text="Yellow", value="yellow"),
                ListItem(text="Green" , value="green" ),
                ListItem(text="Blue"  , value="blue"  ),
                ListItem(text="Indigo", value="indigo"),
                ListItem(text="Violet", value="violet")
              ]
            )
    number1 = Number(document_id="1", page_number="1", x_position="163", y_position="260",
            font="helvetica", font_size="size14", tab_label="numbersOnly",
            width="84", required="false")
    radio_group = RadioGroup(document_id="1", group_name="radio1",
            radios=[
                Radio(page_number="1", x_position="142", y_position="384",
                      value="white", required="false"),
                Radio(page_number="1", x_position="74", y_position="384",
                      value="red", required="false"),
                Radio(page_number="1", x_position="220", y_position="384",
                      value="blue", required="false")
            ])
    text = Text(document_id="1", page_number="1", x_position="153", y_position="230",
            font="helvetica", font_size="size14", tab_label="text",
            height="23", width="84", required="false")
    # Add the tabs model to the signer
    # The Tabs object wants arrays of the different field/tab types
    signer.tabs = Tabs(sign_here_tabs = [sign_here],
                       checkbox_tabs=[check1, check2, check3, check4],
                       list_tabs=[list1], number_tabs=[number1],
                       radio_group_tabs=[radio_group], text_tabs=[text]
    )
    # Create top two objects
    envelope_template_definition = EnvelopeTemplateDefinition(
        description="Example template created via the API",
        name=template_name,
        shared="false"
    )
    # Top object:
    template_request=EnvelopeTemplate(
        documents=[document], email_subject="Please sign this document",
        envelope_template_definition=envelope_template_definition,
        recipients=Recipients(signers=[signer], carbon_copies=[cc]),
        status="created"
    )

    return template_request
# ***DS.snippet.0.end


def get_controller():
    """responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg008_create_template.html",
                               title="Create a template",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG['github_example_url'] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG['documentation'] + eg,
                               show_doc=ds_config.DS_CONFIG['documentation'],
        )
    else:
        # Save the current operation so it will be resumed after authentication
        session['eg'] = url_for(eg)
        return redirect(url_for('ds_must_authenticate'))


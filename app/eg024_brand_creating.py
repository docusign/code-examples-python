"""Example 024: Creating a brand"""

import json
from os import path

from docusign_esign import ApiClient, AccountsApi, Brand
from docusign_esign.client.api_exception import ApiException
from flask import render_template, url_for, redirect, session, flash, request

from app import app, ds_config, views

eg = 'eg024'    # reference and url for this example

LANGUAGES = {
        "Arabic": "ar",
        "Armenian": "hy",
        "Bahasa Indonesia": "id",
        "Bahasa Malay": "ms",
        "Bulgarian": "bg",
        "Chinese Simplified": "zh_CN",
        "Chinese Traditional": "zh_TW",
        "Croatian": "hr",
        "Czech": "cs",
        "Danish": "da",
        "Dutch": "nl",
        "English UK": "en_GB",
        "English US": "en",
        "Estonian": "et",
        "Farsi": "fa",
        "Finnish": "fi",
        "French": "fr",
        "French Canada": "fr_CA",
        "German": "de",
        "Greek": "el",
        "Hebrew": "he",
        "Hindi": "hi",
        "Hungarian": "hu",
        "Italian": "it",
        "Japanese": "ja",
        "Korean": "ko",
        "Latvian": "lv",
        "Lithuanian": "lt",
        "Norwegian": "no",
        "Polish": "pl",
        "Portuguese": "pt",
        "Portuguese Brasil": "pt_BR",
        "Romanian": "ro",
        "Russian": "ru",
        "Serbian": "sr",
        "Slovak": "sk",
        "Slovenian": "sl",
        "Spanish": "es",
        "Spanish Latin America": "es_MX",
        "Swedish": "sv",
        "Thai": "th",
        "Turkish": "tr",
        "Ukrainian": "uk",
        "Vietnamese": "vi"
    }


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
        # Step 1: Obtain your OAuth token
        args = {
            'account_id': '213',  # represent your {ACCOUNT_ID}
            'base_path': session['ds_base_path'],
            'access_token': session['ds_access_token'],   # represent your {ACCESS_TOKEN}
            'brand_name': request.form.get('brand_name'),
            'default_language': request.form.get('default_language')
        }
        try:
            # Step 2: Call the worker method to create a new brand
            response = worker(args)
            brand_id = response.brands[0].brand_id
            app.logger.info(f"Brand has been created. Brand id {brand_id}")

            # Step 3: Render response
            return render_template('example_done.html',
                                   title='Brand creating',
                                   h1='Brand creating',
                                   message=f"""The brand has been created and sent!<br/>
                                               Brand ID {brand_id}."""
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
    1. Create api client with headers
    2. Create a brand object
    3. Post the brand using SDK
    """

    # Step 1: create API client
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {args['access_token']}")

    # Step 2: Create a brand object
    brand = Brand(
        brand_name=args['brand_name'],
        default_brand_language=args['default_language'],
    )

    # Step 3: a) Call the eSignature SDK
    # b) Display the JSON response
    account_api = AccountsApi(api_client)
    response = account_api.create_brand(account_id=args['account_id'], brand=brand)
    return response


def get_controller():
    """Responds with the form for the example"""

    if views.ds_token_ok():
        return render_template("eg024_brand_creating.html",
                               title="Brand creating",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               languages=LANGUAGES
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))

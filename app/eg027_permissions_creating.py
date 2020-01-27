"""Example 027: Creating a permissions profile settings"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views, constants
import json
from docusign_esign import ApiClient, AccountsApi, PermissionProfile
from docusign_esign.client.api_exception import ApiException

eg = 'eg027'


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
        settings = constants.settings
        # Map all settings except defaults to apply values from UI
        for setting in settings:
            value = request.form.get(setting)
            if value:
                settings[setting] = value
            elif not settings[setting]:
                settings[setting] = 'false'

        # Step 1: Obtain your OAuth token
        args = {
            'account_id': session['ds_account_id'],  # represent your {ACCOUNT_ID}
            'base_path': session['ds_base_path'],
            'access_token': session['ds_access_token'],  # represent your {ACCESS_TOKEN}
            'permission_profile_name': request.form.get('permission_profile_name'),
            'settings': settings
        }

        try:
            # Step 2: Call worker method to create a permission profile
            response = worker(args)
            permission_profile_id = response.permission_profile_id
            app.logger.info(f"Permission profile has been created. Permission id: {permission_profile_id}")

            return render_template('example_done.html',
                                   title='Creating a permission profile',
                                   h1='Creating a permission profile',
                                   message=f"""Permission profile has been created!<br/>
                                                Permission profile ID: {permission_profile_id}."""
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
    1. Create api client
    2. Create permission profile object
    3. Create permission profile using SDK
    """

    # Step 1: Create api client and add headers to it
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {args['access_token']}")

    # Step 2: Create permission profile object
    permission_profile = PermissionProfile(
        permission_profile_name=args['permission_profile_name'],
        settings=args['settings']
    )

    # Step 3: Create permission profile with AccountPermissionProfiles:: create
    account_api = AccountsApi(api_client)
    response = account_api.create_permission_profile(args['account_id'], permission_profile=permission_profile)

    return response


def get_controller():
    """Responds with the form for the example"""
    if views.ds_token_ok():
        return render_template("eg027_permissions_creating.html",
                               title="Creating a permission profile",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               permission_profile_name='Sample Profile 134972-Alpha'
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


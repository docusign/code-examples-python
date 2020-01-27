"""Example 028: Deleting a permission profile"""

from flask import render_template, url_for, redirect, session, flash, request
from os import path
from app import app, ds_config, views
import json
from docusign_esign import ApiClient, AccountsApi
from docusign_esign.client.api_exception import ApiException

eg = 'eg028'


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
    """
    minimum_buffer_min = 3
    if views.ds_token_ok(minimum_buffer_min):
        # Step 1: Obtain your OAuth token
        args = {
            'account_id': session['ds_account_id'],  # represent your {ACCOUNT_ID}
            'base_path': session['ds_base_path'],
            'access_token': session['ds_access_token'],  # represent your {ACCESS_TOKEN}
            'permission_profile_id': request.form.get('permission_profile'),
        }
        try:
            # Step 2: Call the worker method to delete a permission profile
            worker(args)
            app.logger.info(f"Permission profile has been deleted.")

            return render_template('example_done.html',
                                   title='Deleting a permission profile',
                                   h1='Deleting a permission profile',
                                   message=f"Permission profile has been deleted!<br/>"
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
    Step 1: Create an api client
    Step 2: Delete the permission profile using SDK
    """
    api_client = create_api_client(args)

    account_api = AccountsApi(api_client)
    response = account_api.delete_permission_profile(account_id=args['account_id'],
                                                     permission_profile_id=args['permission_profile_id'])

    return response


def get_permissions_profile():
    """Retrieve all permission profiles"""
    args = {
        'account_id': session['ds_account_id'],  # represent your {ACCOUNT_ID}
        'base_path': session['ds_base_path'],
        'access_token': session['ds_access_token'],  # represent your {ACCESS_TOKEN}
    }

    api_client = create_api_client(args)

    try:
        account_api = AccountsApi(api_client)
        response = account_api.list_permissions(args['account_id'])

        return response.permission_profiles

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


def create_api_client(args):
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = args['base_path']
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {args['access_token']}")

    return api_client


def get_controller():
    """Responds with the form for the example"""
    if views.ds_token_ok():
        permission_profiles = get_permissions_profile()
        return render_template("eg028_permissions_delete.html",
                               title="Deleting a permission profile",
                               source_file=path.basename(__file__),
                               source_url=ds_config.DS_CONFIG["github_example_url"] + path.basename(__file__),
                               documentation=ds_config.DS_CONFIG["documentation"] + eg,
                               show_doc=ds_config.DS_CONFIG["documentation"],
                               permission_profiles=permission_profiles
                               )
    else:
        # Save the current operation so it will be resumed after authentication
        session["eg"] = url_for(eg)
        return redirect(url_for("ds_must_authenticate"))


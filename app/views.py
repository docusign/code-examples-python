from flask import render_template, url_for, redirect, session, flash
from flask_oauthlib.client import OAuth
from app import app
from app import ds_config
from datetime import datetime, timedelta
import requests

base_uri_suffix = '/restapi'
oauth = OAuth(app)
docusign = oauth.remote_app(
    'docusign',
    consumer_key=ds_config.DS_CONFIG['ds_client_id'],
    consumer_secret=ds_config.DS_CONFIG['ds_client_secret'],
    access_token_url=ds_config.DS_CONFIG['authorization_server'] + '/oauth/token',
    authorize_url=ds_config.DS_CONFIG['authorization_server'] + '/oauth/auth',
    request_token_params={'scope': 'signature'},
    base_url=None,
    request_token_url=None,
    access_token_method='POST'
)


@app.route('/ds/login')
def login():
    return docusign.authorize(callback=url_for('ds_callback', _external=True))


@app.route('/logout')
def logout():
    # remove the keys and their values from the session
    session.pop('ds_access_token', None)
    session.pop('ds_refresh_token', None)
    session.pop('ds_user_email', None)
    session.pop('ds_user_name', None)
    session.pop('ds_expiration', None)
    session.pop('ds_account_id', None)
    session.pop('ds_account_name', None)
    session.pop('ds_basePath', None)

    return redirect(url_for('index'))


@app.route('/ds/callback')
def ds_callback():
    resp = docusign.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    # app.logger.info('Authenticated with DocuSign.')
    flash('You have authenticated with DocuSign.')
    session['ds_access_token'] = resp['access_token']
    session['ds_refresh_token'] = resp['refresh_token']
    session['ds_expiration'] = datetime.utcnow() + timedelta(seconds=resp['expires_in'])

    # Determine user, account_id, base_url by calling OAuth::getUserInfo
    # See https://developers.docusign.com/esign-rest-api/guides/authentication/user-info-endpoints
    url = ds_config.DS_CONFIG['authorization_server'] + '/oauth/userinfo'
    auth = {"Authorization": "Bearer " + session['ds_access_token']}
    response = requests.get(url, headers=auth).json()
    session['ds_user_name'] = response["name"]
    session['ds_user_email'] = response["email"]
    accounts = response["accounts"]
    account = None # the account we want to use
    # Find the account...
    target_account_id = ds_config.DS_CONFIG['target_account_id']
    if target_account_id:
        account = next( (a for a in accounts if a["account_id"] == target_account_id), None)
        if not account:
            # Panic! The user does not have the targeted account. They should not log in!
            raise Exception("No access to target account")
    else:
        account = next((a for a in accounts if a["is_default"]), None)
        if not account:
            # Panic! Every user should always have a default account
            raise Exception("No default account")

    # Save the account information
    session['ds_account_id'] = account["account_id"]
    session['ds_account_name'] = account["account_name"]
    session['ds_basePath'] = account["base_uri"] + base_uri_suffix

    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('home.html', title='Home - Python Code Examples')

@app.route('/index')
def r_index():
    return redirect(url_for('index'))



################################################################################
################################################################################


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


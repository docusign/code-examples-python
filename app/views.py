from flask import render_template, url_for, redirect, session
from flask_oauthlib.client import OAuth
from app import app
from app import ds_config
from datetime import datetime, timedelta
import requests


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
    session.pop('docusign_access_token', None)
    session.pop('docusign_refresh_token', None)
    session.pop('docusign_expiration', None)
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
    session['docusign_access_token'] = resp['access_token']
    session['docusign_refresh_token'] = resp['refresh_token']
    session['docusign_expiration'] = datetime.utcnow() + timedelta(seconds=resp['expires_in'])

    # Determine user, account_id, base_url by calling OAuth::getUserInfo
    # See https://developers.docusign.com/esign-rest-api/guides/authentication/user-info-endpoints
    url = ds_config.DS_CONFIG['authorization_server'] + '/oauth/userinfo'
    auth = {"Authorization": "Bearer " + session['docusign_access_token']}
    response = requests.get(url, headers=auth).json()

    return redirect(url_for('index'))


@docusign.tokengetter
def get_docusign_oauth_token():
    return session.get('docusign_token')



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


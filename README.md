# Multiple DocuSign Signature REST API recipes in Python

Repo: esignature-recipes-python

This is a **beta** release. Comments are welcomed.

This repo contains a Python Flask application that demonstrates several of the
DocuSign Signature REST API recipes:

* Embedded signing. See app/py_001_embedded_signing
* Sending a signature request via email. See app/py_004_email_send
* Sending a signature request using a template. See app/py_002_email_send_template
* Get envelopes’ statuses. See app/py_005_envelope_list_status
* Get an envelope’s status. See app/py_006_envelope_status
* Get an envelope’s recipient statuses. See app/py_007_envelope_recipient_status
* Using a webhook to receive status changes. See app/lib_master_python/ds_webhook.py
* Authenticating with the Signature REST API. See app/lib_master_python/ds_authentication.py
* Embedded tagging and sending of an envelope. See app/py_012_embedded_tagging

## API Logging Feature
The application also enables you to easily view your account’s API logs. It shows all API requests to your
demo account, from this application, and from others including the DocuSign web tool.

## Try it on Heroku
Use the deploy button to immediately try this app on Heroku. You can use Heroku’s free service tier, no credit card is needed.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Integration Key and Secret
**Do not use** the DS_OAUTH_CLIENT_ID or DS_OAUTH_SECRET config variables.

Instead, enter your Integration Key (Client ID) and Secret after you have started the software on Heroku.

Details: the config variables should only be used if the new server's name is already known and has been
registered as a redirect URI with the DocuSign authentication service.

### Build delays
Note: during the Heroku *build* process, the setup.py step for **lxml** takes several minutes since it includes a compilation.

## Run the app locally

1. Install a recent version of Python 2.x, eg 2.7.11 or later.
1. Install pip
1. Clone this repo to your computer
1. `cd` to the repo’s directory
1. `pip install -r requirements.txt` # installs the application’s requirements
1. `python run.py` # starts the application on port 5000
1. Use a browser to load [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Have a question? Pull request?
If you have a question about the Signature REST API, please use StackOverflow and tag your question with `docusignapi`

For bug reports and pull requests, please use this repo’s issues page.

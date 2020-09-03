# Python: Authorization Code Grant Examples

### Github repo: code-examples-python
## Introduction
This repo is a Python 3 application that demonstrates:

* Authentication with DocuSign via the
[Authorization Code Grant flow](https://developers.docusign.com/esign-rest-api/guides/authentication/oauth2-code-grant).
When the token expires, the user is asked to re-authenticate.
The **refresh token** is not used in this example.
1. **Embedded Signing Ceremony.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg001_embedded_signing.py)
   This example sends an envelope, and then uses an embedded signing ceremony for the first signer.
   With embedded signing, the DocuSign signing ceremony is initiated from your website.
1. **Send an envelope with a remote (email) signer and cc recipient.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg002_signing_via_email.py)
   The envelope includes a pdf, Word, and HTML document.
   Anchor text ([AutoPlace](https://support.docusign.com/en/guides/AutoPlace-New-DocuSign-Experience)) is used to position the signing fields in the documents.
1. **List envelopes in the user's account.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg003_list_envelopes.py)
   The envelopes' current status is included.
1. **Get an envelope's basic information.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg004_envelope_info.py)
   The example lists the basic information about an envelope, including its overall status.
1. **List an envelope's recipients**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg005_envelope_recipients.py)
   Includes current recipient status.
1. **List an envelope's documents.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg006_envelope_docs.py)
1. **Download an envelope's documents.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg007_envelope_get_doc.py)
   The example can download individual
   documents, the documents concatenated together, or a zip file of the documents.
1. **Programmatically create a template.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg008_create_template.py)
1. **Send an envelope using a template.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg009_use_template.py)
1. **Send an envelope and upload its documents with multpart binary transfer.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg010_send_binary_docs.py)
   Binary transfer is 33% more efficient than using Base64 encoding.
1. **Embedded sending.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg011_embedded_sending.py)
   Embeds the DocuSign web tool (NDSE) in your web app to finalize or update
   the envelope and documents before they are sent.
1. **Embedded DocuSign web tool (NDSE).**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg012_embedded_console.py)
1. **Embedded Signing Ceremony from a template with an added document.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg013_add_doc_to_template.py)
   This example sends an envelope based on a template.
   In addition to the template's document(s), the example adds an
   additional document to the envelope by using the
   [Composite Templates](https://developers.docusign.com/esign-rest-api/guides/features/templates#composite-templates)
   feature.
1. **Payments example: an order form, with online payment by credit card.**
   [Source.](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/app/eg014_collect_payment.py)
1. **Get the envelope tab data.**
   Retrieve the tab (field) values for all of the envelope's recipients.
   [Source.](./app/eg015_envelope_tab_data.py)
1. **Set envelope tab values.**
   The example creates an envelope and sets the initial values for its tabs (fields). Some of the tabs
   are set to be read-only, others can be updated by the recipient. The example also stores
   metadata with the envelope.
   [Source.](./app/eg016_set_tab_values.py)
1. **Set template tab values.**
   The example creates an envelope using a template and sets the initial values for its tabs (fields).
   The example also stores metadata with the envelope.
   [Source.](./app/eg017_set_template_tab_values.py)
1. **Get the envelope custom field data (metadata).**
   The example retrieves the custom metadata (custom data fields) stored with the envelope.
   [Source.](./app/eg018_envelope_custom_field_data.py)
1. **Requiring an Access Code for a Recipient**
   [Source.](./app/eg019_access_code_authentication.py)
   This example sends an envelope that requires an access-code for the purpose of multi-factor authentication.   
1. **Requiring SMS authentication for a recipient**
   [Source.](./app/eg020_sms_authentication.py)
   This example sends an envelope that requires entering in a six digit code from an text message for the purpose of multi-factor authentication.   
1. **Requiring Phone authentication for a recipient**
   [Source.](./app/eg013_add_doc_to_template.py)
   This example sends an envelope that requires entering in a voice-based response code for the purpose of multi-factor authentication.  
1. **Requiring Knowledge-Based Authentication (KBA) for a Recipient**
   [Source.](./app/eg022_kba_authentication.py)
   This example sends an envelope that requires passing a Public records check to validate identity for the purpose of multi-factor authentication.    


## Installation

### Prerequisites
1. A DocuSign Developer Sandbox account (email and password) on [demo.docusign.net](https://demo.docusign.net).
   Create a [free account](https://go.docusign.com/sandbox/productshot/?elqCampaignId=16535).
1. A DocuSign Integration Key (a client ID) that is configured to use the
   OAuth Authorization Code flow.
   You will need the **Integration Key** itself, and its **secret**.

   If you use this example on your own workstation,
   the Integration key must include a **Redirect URI** of `http://localhost:5000/ds/callback`

   If you will not be running the example on your own workstation,
   use the appropriate DNS name and port instead of `localhost`
   
   This [**video**](https://www.youtube.com/watch?v=eiRI4fe5HgM)
   demonstrates how to create an Integration Key (client id) for a
   user application like this example. Note that the redirect url for your 
   Integration Key will be `http://localhost:5000/ds/callback` if you
   use the default Python settings.

1. Python 3.
1. A name and email for a signer, and a name and email for a cc recipient.

### Installation steps
1. Download or clone this repository to your workstation to directory **code-examples-python**
1. **cd code-examples-python**
1. **pip3 install -r requirements.txt**  (or pipenv can be used)
1. Update the file **app/ds_config.py**
     with the Integration Key and other settings.

   **Note:** Protect your Integration Key and secret--you
   should ensure that ds_config.py file will not be stored in your source code
   repository.

1. **python3 run.py**
1. Open a browser to **http://localhost:5000**

#### Payments code example
To use the payments example, create a
test payments gateway for your developer sandbox account.

See the
[PAYMENTS_INSTALLATION.md](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/PAYMENTS_INSTALLATION.md)
file for instructions.

Then add the payment gateway account id to the **app/ds_config.py** file.

## Using the examples with other authentication flows

The examples in this repository can also be used with either the
Implicit Grant or JWT OAuth flows.
See the [Authentication guide](https://developers.docusign.com/esign-rest-api/guides/authentication)
for information on choosing the right authentication flow for your application.

## License and additional information

### License
This repository uses the MIT License. See the LICENSE file for more information.

### Pull Requests
Pull requests are welcomed. Pull requests will only be considered if their content
uses the MIT License.

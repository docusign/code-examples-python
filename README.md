# Python Launcher Code Examples

### Github repo: [code-examples-python](./)
## Introduction
This repo is a Python 3 application that demonstrates:


1. **Embedded Signing Ceremony.**
   [Source.](./app/examples/eg001_embedded_signing/controller.py)
   This example sends an envelope, and then uses an embedded signing ceremony for the first signer.
   With embedded signing, the DocuSign signing ceremony is initiated from your website.
1. **Send an envelope with a remote (email) signer and cc recipient.**
   [Source.](./app/examples/eg002_signing_via_email/controller.py)
   The envelope includes a pdf, Word, and HTML document.
   Anchor text ([AutoPlace](https://support.docusign.com/en/guides/AutoPlace-New-DocuSign-Experience)) is used to position the signing fields in the documents.
1. **List envelopes in the user's account.**
   [Source.](./app/examples/eg003_list_envelopes/controller.py)
   The envelopes' current status is included.
1. **Get an envelope's basic information.**
   [Source.](./app/examples/eg004_envelope_info/controller.py)
   The example lists the basic information about an envelope, including its overall status.
1. **List an envelope's recipients**
   [Source.](./app/examples/eg005_envelope_recipients/controller.py)
   Includes current recipient status.
1. **List an envelope's documents.**
   [Source.](./app/examples/eg006_envelope_docs/controller.py)
1. **Download an envelope's documents.**
   [Source.](./app/examples/eg007_envelope_get_doc/controller.py)
   The example can download individual
   documents, the documents concatenated together, or a zip file of the documents.
1. **Programmatically create a template.**
   [Source.](./app/examples/eg008_create_template/controller.py)
1. **Send an envelope using a template.**
   [Source.](./app/examples/eg009_use_template/controller.py)
1. **Send an envelope and upload its documents with multipart binary transfer.**
   [Source.](./app/examples/eg010_send_binary_docs/controller.py)
   Binary transfer is 33% more efficient than using Base64 encoding.
1. **Embedded sending.**
   [Source.](./app/examples/eg011_embedded_sending/controller.py)
   Embeds the DocuSign web tool (NDSE) in your web app to finalize or update
   the envelope and documents before they are sent.
1. **Embedded DocuSign web tool (NDSE).**
   [Source.](./app/examples/eg012_embedded_console/controller.py)
1. **Embedded Signing Ceremony from a template with an added document.**
   [Source.](./app/examples/eg013_add_doc_to_template/controller.py)
   This example sends an envelope based on a template.
   In addition to the template's document(s), the example adds an
   additional document to the envelope by using the
   [Composite Templates](https://developers.docusign.com/esign-rest-api/guides/features/templates#composite-templates)
   feature.
1. **Payments example: an order form, with online payment by credit card.**
   [Source.](./app/examples/eg014_collect_payment/controller.py)
1. **Get the envelope tab data.**
   Retrieve the tab (field) values for all of the envelope's recipients.
   [Source.](./app/examples/eg015_envelope_tab_data/controller.py)
1. **Set envelope tab values.**
   The example creates an envelope and sets the initial values for its tabs (fields). Some of the tabs
   are set to be read-only, others can be updated by the recipient. The example also stores
   metadata with the envelope.
   [Source.](./app/examples/eg016_set_tab_values/controller.py)
1. **Set template tab values.**
   The example creates an envelope using a template and sets the initial values for its tabs (fields).
   The example also stores metadata with the envelope.
   [Source.](./app/examples/eg017_set_template_tab_values/controller.py)
1. **Get the envelope custom field data (metadata).**
   The example retrieves the custom metadata (custom data fields) stored with the envelope.
   [Source.](./app/examples/eg018_envelope_custom_field_data/controller.py)
1. **Requiring an Access Code for a Recipient**
   [Source.](./app/examples/eg019_access_code_authentication/controller.py)
   This example sends an envelope that requires an access-code for the purpose of multi-factor authentication.   
1. **Requiring SMS authentication for a recipient**
   [Source.](./app/examples/eg020_sms_authentication/controller.py)
   This example sends an envelope that requires entering in a six digit code from an text message for the purpose of multi-factor authentication.   
1. **Requiring Phone authentication for a recipient**
   [Source.](./app/examples/eg021_phone_authentication/controller.py)
   This example sends an envelope that requires entering in a voice-based response code for the purpose of multi-factor authentication. 
1. **Requiring Knowledge-Based Authentication (KBA) for a Recipient**
   [Source.](./app/examples/eg022_kba_authentication/controller.py)
   This example sends an envelope that requires passing a Public records check to validate identity for the purpose of multi-factor authentication.    
1. **Requiring ID Verification (IDV) for a recipient**
   [Source.](./app/examples/eg023_idv_authentication/controller.py)
   This example sends an envelope that requires submitting a photo of a government issued id for the purpose of multi-factor authentication.
1. **Creating a permission profile**
   [Source.](./app/examples/eg024_permissions_creating/controller.py)
   This code example demonstrates how to create a permission profile using the [Create Permission Profile](https://developers.docusign.com/esign-rest-api/reference/Accounts/AccountPermissionProfiles/create) method.
1. **Setting a permission profile**
   [Source.](./app/examples/eg025_permissions_set_user_group/controller.py)
   This code example demonstrates how to set a user group’s permission profile using the [Update Group](https://developers.docusign.com/esign-rest-api/reference/UserGroups/Groups/update) method. 
   You must have already created the permissions profile and the group of users.
1. **Updating individual permission settings**
   [Source.](./app/examples/eg026_permissions_change_single_setting/controller.py)
   This code example demonstrates how to edit individual permission settings on a permissions profile using the [Update Permission Profile](https://developers.docusign.com/esign-rest-api/reference/Accounts/AccountPermissionProfiles/update) method.
1. **Deleting a permission profile**
   [Source.](./app/examples/eg027_permissions_delete/controller.py)
   This code example demonstrates how to delete a permission profile using the [Delete Permission Profile](https://developers.docusign.com/esign-rest-api/reference/Accounts/AccountPermissionProfiles/create) method.
1. **Creating a brand**
   [Source.](./app/examples/eg028_brand_creating/controller.py)
   This example creates brand profile for an account using the [Create Brand](https://developers.docusign.com/esign-rest-api/reference/Accounts/AccountBrands/create) method.
1. **Applying a brand to an envelope**
   [Source.](./app/examples/eg029_brands_apply_to_envelope/controller.py)
   This code example demonstrates how to apply a brand you've created to an envelope using the [Create Envelope](https://developers.docusign.com/esign-rest-api/reference/Envelopes/Envelopes/create) method. 
   First, creates the envelope and then applies the brand to it.
   Anchor text ([AutoPlace](https://support.docusign.com/en/guides/AutoPlace-New-DocuSign-Experience)) is used to position the signing fields in the documents.
1. **Applying a brand to a template**
   [Source.](./app/examples/eg030_brands_apply_to_template/controller.py)
   This code example demonstrates how to apply a brand you've created to a template using using the [Create Envelope](https://developers.docusign.com/esign-rest-api/reference/Envelopes/Envelopes/create) method. 
   You must have already created the template and the brand.
   Anchor text ([AutoPlace](https://support.docusign.com/en/guides/AutoPlace-New-DocuSign-Experience)) is used to position the signing fields in the documents.
1. **Bulk sending envelopes to multiple recipients**
   [Source.](./app/examples/eg031_bulk_send/controller.py)
   This code example demonstrates how to send envelopes in bulk to multiple recipients using these methods:
   [Create Bulk Send List](https://developers.docusign.com/esign-rest-api/reference/BulkEnvelopes/BulkSend/createBulkSendList), 
   [Create Bulk Send Request](https://developers.docusign.com/esign-rest-api/reference/BulkEnvelopes/BulkSend/createBulkSendRequest).
   Firstly, creates a bulk send recipients list, and then creates an envelope. 
   After that, initiates bulk envelope sending.


## Included OAuth grant types:

* Authentication with Docusign via [Authorization Code Grant flow](https://developers.docusign.com/esign-rest-api/guides/authentication/oauth2-code-grant) .
When the token expires, the user is asked to re-authenticate.
The **refresh token** is not used in this example.

* Authentication with DocuSign via the [JSON Web Token (JWT) Grant](https://developers.docusign.com/esign-rest-api/guides/authentication/oauth2-jsonwebtoken).
When the token expires, it updates automatically.


## Installation

### Prerequisites
1. A DocuSign Developer Sandbox account (email and password) on [demo.docusign.net](https://demo.docusign.net).
   Create a [free account](https://go.docusign.com/sandbox/productshot/?elqCampaignId=16535).
1. A DocuSign Integration Key (a client ID). To use Authorization code grant, you will need the **Integration Key** itself, and its **secret**. To use JSON Web token, you will need the **Integration Key** itself, the **RSA Secret Key** and an API user ID for the user you are impersonating.  

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
1. Download or clone this repository to your workstation to directory **eg-03-python-auth-code-grant**
1. **cd eg-03-python-auth-code-grant**
1. **pip3 install -r requirements.txt**  (or pipenv can be used)
1. Make a copy of the **app/ds_config_sample.py** and name it **ds_config.py** 
1. Update this new file **app/ds_config.py**
     with your Integration Key and other settings.

   **Note:** Protect your Integration Key and secret--you
   should ensure that ds_config.py file will not be stored in your source code
   repository.

1. **python run.py**
1. Open a browser to **http://localhost:5000**

### Configuring JWT

1. Create a developer sandbox account on developers.docusign.com if you don't already have one.
2. Create a new API key in the Admin panel: https://admindemo.docusign.com/api-integrator-key, take note of the public key.
3. Set a redirect URI of `http://localhost:5000/ds/callback` as mentioned in the installation steps above for the API key you make in step 2.
4. Generate an RSA keypair in the administrator console on the DocuSign developer sandbox and copy the private key to a secure location.
5. Create a new file in your repo source folder named **private.key**, and paste in that copied RSA private key, then save it.
6. Update the file **app/ds_config.py** and include the newly created API key from step 2 as well as your account user id GUID which is also found on the Admin panel: `https://admindemo.docusign.com/api-integrator-key`.

From there you should be able to run the launcher using **python run.py** then selecting **JSON Web Token** when authenticaing your account.

#### Payments code example
To use the payments example, create a
test payments gateway for your developer sandbox account.

See the
[PAYMENTS_INSTALLATION.md](https://github.com/docusign/eg-03-python-auth-code-grant/blob/master/PAYMENTS_INSTALLATION.md)
file for instructions.

Then add the payment gateway account id to the **app/ds_config.py** file.



## License and additional information

### Implicit Grant

The examples in this repository can also be used with the
Implicit Grant OAuth flow.
See the [Authentication guide](https://developers.docusign.com/esign-rest-api/guides/authentication)
for information on choosing the right authentication flow for your application.

### License
This repository uses the MIT License. See the LICENSE file for more information.

### Pull Requests
Pull requests are welcomed. Pull requests will only be considered if their content
uses the MIT License.
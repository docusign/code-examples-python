# Python Launcher Code Examples

### Github repo: [code-examples-python](./)

This GitHub repo includes code examples for the DocuSign eSignature REST API, Rooms API, and Click API. To switch between API code examples, modify the EXAMPLES_API_TYPE setting in the ds_config.py file. Change the value of either `ESignature`, `Rooms`, `Click`, or `Monitor` to `"true"` to use the corresponding API. Set only one API type to true and set the remaining to false.

If none of the API types are set to true, the DocuSign eSignature REST API code examples will be shown. If multiple API types are set to true, only the first will be shown.


## Introduction

This repo is a Python 3 application that supports the following authentication workflows:

* Authentication with DocuSign via [Authorization Code Grant](https://developers.docusign.com/platform/auth/authcode).
When the token expires, the user is asked to re-authenticate. The refresh token is not used.

* Authentication with DocuSign via [JSON Web Token (JWT) Grant](https://developers.docusign.com/platform/auth/jwt/).
When the token expires, it updates automatically.

## eSignature API

For more information about the scopes used for obtaining authorization to use the eSignature API, see [Required scopes](https://developers.docusign.com/docs/esign-rest-api/esign101/auth#required-scopes).

For a list of code examples that use the eSignature API, select the Python tab under [Examples and languages](https://developers.docusign.com/docs/esign-rest-api/how-to/code-launchers#examples-and-languages) the DocuSign Developer Center.

## Rooms API

**Note:** To use the Rooms API you must also [create your Rooms developer account](https://developers.docusign.com/docs/rooms-api/rooms101/create-account). Examples 4 and 6 require that you have the DocuSign Forms feature enabled in your Rooms for Real Estate account.  
For more information about the scopes used for obtaining authorization to use the Rooms API, see [Required scopes](https://developers.docusign.com/docs/rooms-api/rooms101/auth/). 

For a list of code examples that use the Rooms API, select the Python tab under [Examples and languages](https://developers.docusign.com/docs/rooms-api/how-to/code-launchers#examples-and-languages) on the DocuSign Developer Center.
 
## Click API

For more information about the scopes used for obtaining authorization to use the Click API, see [Required scopes](https://developers.docusign.com/docs/click-api/click101/auth/#required-scopes).

For a list of code examples that use the Click API, select the Python tab under [Examples and languages](https://developers.docusign.com/docs/click-api/how-to/code-launchers#examples-and-languages) on the DocuSign Developer Center.

## Monitor API
**Note:** To use the Monitor API, you must also [enable DocuSign Monitor for your organization](https://developers.docusign.com/docs/monitor-api/how-to/enable-monitor/).   
For information about the scopes used for obtaining authorization to use the Monitor API, see [Required scopes](https://developers.docusign.com/docs/monitor-api/monitor101/auth/).

For a list of code examples that use the Monitor API, select the Python tab under [Examples and languages](https://developers.docusign.com/docs/monitor-api/how-to/code-launchers/#examples-and-languages) on the DocuSign Developer Center.

## Installation

### Prerequisites
**Note:** If you downloaded this code using [Quickstart](https://developers.docusign.com/docs/esign-rest-api/quickstart/) from the DocuSign Developer Center, skip items 1 and 2 as they were automatically performed for you.

1. A free [DocuSign developer account](https://go.docusign.com/o/sandbox/); create one if you don't already have one.
1. A DocuSign app and integration key that is configured to use either [Authorization Code Grant](https://developers.docusign.com/platform/auth/authcode/) or [JWT Grant](https://developers.docusign.com/platform/auth/jwt/) authentication.

   This [video](https://www.youtube.com/watch?v=eiRI4fe5HgM) demonstrates how to obtain an integration key.  
   
   To use [Authorization Code Grant](https://developers.docusign.com/platform/auth/authcode/), you will need an integration key and a secret key. See [Installation steps](#installation-steps) for details.  

   To use [JWT Grant](https://developers.docusign.com/platform/auth/jwt/), you will need an integration key, an RSA key pair, and the API Username GUID of the impersonated user. See [Installation steps for JWT Grant authentication](#installation-steps-for-jwt-grant-authentication) for details.  

   For both authentication flows:  
   
   If you use this launcher on your own workstation, the integration key must include redirect a URI of http://localhost:5000/ds/callback

   If you host this launcher on a remote web server, set your redirect URI as   
   
   {base_url}/ds/callback
   
   where {base_url} is the URL for the web app.

1. Python 3.

### Installation steps

**Note:** If you downloaded this code using [Quickstart](https://developers.docusign.com/docs/esign-rest-api/quickstart/) from the DocuSign Developer Center, skip step 4 as it was automatically performed for you.

1. Extract the Quickstart ZIP file or download or clone the code-examples-python repository.
1. In your command-line environment, switch to the folder:  
   `cd <Quickstart folder>` or `cd code-examples-python`
1. To install dependencies, run  `pip3 install -r requirements.txt`  (or pipenv can be used).
1. To configure the launcher for [Authorization Code Grant](https://developers.docusign.com/platform/auth/authcode/) authentication, create a copy of the file app/ds_config_sample.py and save the copy as app/ds_config.py.
   1. Add your integration key. On the [Apps and Keys](https://admindemo.docusign.com/authenticate?goTo=apiIntegratorKey) page, under **Apps and Integration Keys**, choose the app to use, then select **Actions > Edit**. Under **General Info**, copy the **Integration Key** GUID and save it in ds_config.py as your `ds_client_id`.
   1. Generate a secret key, if you don’t already have one. Under **Authentication**, select **+ ADD SECRET KEY**. Copy the secret key and save it in ds_config.py as your `ds_client_secret`.
   1. Add the launcher’s redirect URI. Under **Additional settings**, select **+ ADD URI**, and set a redirect URI of http://localhost:5000/ds/callback. Select **SAVE**.   
   1. Set a name and email address for the signer. In ds_config.py, save an email address as `signer_email` and a name as `signer_name`.  
**Note:** Protect your personal information. Please make sure that ds_config.py will not be stored in your source code repository.
1. Run the launcher:`python run.py`
   **Note:** You will need to alias the python command to run Python 3 or use `python3 run.py`
1. Open a browser to http://localhost:5000

### Installation steps for JWT Grant authentication

**Note:** If you downloaded this code using [Quickstart](https://developers.docusign.com/docs/esign-rest-api/quickstart/) from the DocuSign Developer Center, skip step 4 as it was automatically performed for you.  
Also, in order to select JSON Web Token authentication in the launcher, in app/ds_config.py, change the `quickstart` setting to `"false"`.

1. Extract the Quickstart ZIP file or download or clone the code-examples-python repository.
1. In your command-line environment, switch to the folder: `cd <Quickstart folder>` or `cd code-examples-python`
1. To install dependencies, run `pip3 install -r requirements.txt`  (or pipenv can be used).
1. To configure the launcher for [JWT Grant](https://developers.docusign.com/platform/auth/jwt/) authentication, create a copy of the file app/ds_config_sample.py and save the copy as app/ds_config.py.
   1. Add your API Username. On the [Apps and Keys](https://admindemo.docusign.com/authenticate?goTo=apiIntegratorKey) page, under **My Account Information**, copy the **API Username** GUID and save it in ds_config.py as your `ds_impersonated_user_id`.
   1. Add your integration key. On the [Apps and Keys](https://admindemo.docusign.com/authenticate?goTo=apiIntegratorKey) page, under **Apps and Integration Keys**, choose the app to use, then select **Actions > Edit**. Under **General Info**, copy the **Integration Key** GUID and save it in ds_config.py as your `ds_client_id`.
   1. Generate an RSA key pair, if you don’t already have one. Under **Authentication**, select **+ GENERATE RSA**. Copy the private key, and save it in a new file named app/private.key.   
   1. Add the launcher’s redirect URI. Under **Additional settings**, select **+ ADD URI**, and set a redirect URI of http://localhost:5000/ds/callback. Select **SAVE**.   
   1. Set a name and email address for the signer. In ds_config.py, save an email address as `signer_email` and a name as `signer_name`.  
**Note:** Protect your personal information. Please make sure that ds_config.py will not be stored in your source code repository.  
1. Run the launcher:`python run.py`
   **Note:** You will need to alias the python command to run Python 3 or use `python3 run.py`   
1. Open a browser to http://localhost:5000
1. On the black navigation bar, select **Login**.
1. From the picklist, select **JSON Web Token** > **Authenticate with DocuSign**.
1. When prompted, log in to your DocuSign developer account. If this is your first time using the app, select **ACCEPT** at the consent window. 
3. Select your desired code example.

## Payments code example  

To use the payments code example, create a test payment gateway on the [**Payments**](https://admindemo.docusign.com/authenticate?goTo=payments) page in your developer account. See [Configure a payment gateway](./PAYMENTS_INSTALLATION.md) for details.

Once you've created a payment gateway, save the **Gateway Account ID** GUID to ds_config.py.


## License and additional information  

### License  
This repository uses the MIT License. See [LICENSE](./LICENSE) for details.

### Pull Requests
Pull requests are welcomed. Pull requests will only be considered if their content
uses the MIT License.
from docusign_esign import AccountsApi, Brand
from flask import session, request
from ...docusign import create_api_client

class Eg028BrandCreatingController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "brand_name": request.form.get("brand_name"),
            "default_language": request.form.get("default_language")
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create a brand object
        3. Post the brand using SDK
        """

        # Step 2. Construct your API headers
        #ds-snippet-start:eSign28Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign28Step2

        # Step 3. Construct your request body
        #ds-snippet-start:eSign28Step3
        brand = Brand(
            brand_name=args["brand_name"],
            default_brand_language=args["default_language"],
        )
        #ds-snippet-end:eSign28Step3

        # Step 4. Call the eSignature REST API
        #ds-snippet-start:eSign28Step4
        account_api = AccountsApi(api_client)
        response = account_api.create_brand(account_id=args["account_id"], brand=brand)
        #ds-snippet-end:eSign28Step4
        return response
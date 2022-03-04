from docusign_esign import EnvelopesApi, EnvelopeDefinition, TemplateRole, AccountsApi, TemplatesApi
from docusign_esign.client.api_exception import ApiException
from flask import session, request

from ...consts import pattern
from ...docusign import create_api_client
from ...error_handlers import process_error


class Eg030BrandsApplyToTemplateController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        # More data validation would be a good idea here
        # Strip anything other than the characters listed
        signer_email = pattern.sub("", request.form.get("signer_email"))
        signer_name = pattern.sub("", request.form.get("signer_name"))
        cc_email = request.form.get("cc_email")
        cc_name = request.form.get("cc_name")
        brand_id = request.form.get("brand")
        template_id = session["template_id"]

        if cc_email and cc_name:
            cc_email = pattern.sub("", cc_email)
            cc_name = pattern.sub("", cc_name)

        args = {
            "account_id": session["ds_account_id"],  # represent your {ACCOUNT_ID}
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],  # represent your {ACCESS_TOKEN}
            "envelope_args": {
                "signer_name": signer_name,
                "signer_email": signer_email,
                "cc_name": cc_name,
                "cc_email": cc_email,
                "brand_id": brand_id,
                "template_id": template_id
            }
        }

        return args

    @classmethod
    def worker(cls, args):
        """
        1. Create an api client
        2. Create an envelope definition object
        3. Apply the brand to the envelope using the SDK
        """

        # Step 2. Construct your API headers
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        # Step 3. Construct your request body
        envelope_api = EnvelopesApi(api_client)
        envelope_definition = cls.make_envelope(args["envelope_args"])

        # Step 4. Call the eSignature REST API
        response = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)

        return response

    @classmethod
    def make_envelope(cls, args):
        """
        Creates the envelope definition object
        """
        # Create the envelope definition
        envelope_definition = EnvelopeDefinition(
            status="sent",
            template_id=args["template_id"],
            brand_id=args["brand_id"]
        )

        signer = TemplateRole(
            email=args["signer_email"],
            name=args["signer_name"],
            role_name="signer"
        )

        # In case, we have cc we add him to envelope definition
        if args["cc_email"] and args["cc_name"]:
            cc = TemplateRole(
                email=args["cc_email"],
                name=args["cc_name"],
                role_name="cc"
            )

            envelope_definition.template_roles = [signer, cc]

        else:
            envelope_definition.template_roles = [signer]

        return envelope_definition

    @staticmethod
    def get_data(args):
        """Retrieve brands"""
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])

        try:
            """Retrieve all brands using the AccountBrands::List"""
            account_api = AccountsApi(api_client)
            brands = account_api.list_brands(account_id=args["account_id"]).brands

            return brands

        except ApiException as err:
            return process_error(err)

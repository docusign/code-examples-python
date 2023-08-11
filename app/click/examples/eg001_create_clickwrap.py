import base64
from os import path

from docusign_click import AccountsApi, ClickwrapRequest, DisplaySettings, \
    Document
from flask import session, request

from ...consts import demo_docs_path
from ...ds_config import DS_CONFIG
from ..utils import create_click_api_client


class Eg001CreateClickwrapController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
            "clickwrap_name": request.form.get("clickwrap_name"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create a display settings model
        3. Create a document model
        4. Create a clickwrap request model
        5. Create a clickwrap using SDK
        """
        # Create an API client with headers
        #ds-snippet-start:Click1Step2
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )
        #ds-snippet-end
        
        #ds-snippet-start:Click1Step3
        # Create a display settings model
        display_settings = DisplaySettings(
            consent_button_text="I Agree",
            display_name="Terms of Service",
            downloadable=True,
            format="modal",
            must_read=True,
            require_accept=True,
            document_display="document"
        )

        # Read file from a local directory
        # The reads could raise an exception if the file is not available!
        with open(path.join(demo_docs_path, DS_CONFIG["doc_terms_pdf"]),
                  "rb") as file:
            doc_docx_bytes = file.read()
        doc_b64 = base64.b64encode(doc_docx_bytes).decode("ascii")

        # Create a document model.
        document = Document(  # Create the DocuSign document object
            document_base64=doc_b64,
            document_name="Terms of Service",  # Can be different from actual file name
            file_extension="pdf",  # Many different document types are accepted
            order=0
        )

        # Create a clickwrap request model
        clickwrap_request = ClickwrapRequest(
            display_settings=display_settings,
            documents=[document, ],
            name=args.get("clickwrap_name"),
            require_reacceptance=True
        )
        #ds-snippet-end:Click1Step3

        # Create a clickwrap using SDK
        #ds-snippet-start:Click1Step4
        accounts_api = AccountsApi(api_client)
        response = accounts_api.create_clickwrap(
            clickwrap_request=clickwrap_request,
            account_id=args["account_id"]
        )
        #ds-snippet-end:Click1Step4

        return response

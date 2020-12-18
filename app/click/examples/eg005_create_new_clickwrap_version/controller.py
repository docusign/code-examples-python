import base64
from os import path

from docusign_click import AccountsApi, ClickwrapRequest, DisplaySettings, \
    Document
from flask import session

from ....consts import demo_docs_path
from ....ds_config import DS_CONFIG
from ...utils import create_click_api_client


class Eg005Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
            "clickwrap_id": session.get("clickwrap_id"),
            "clickwrap_name": session.get("clickwrap_name"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Create a display settings model
        3. Create a document model.
        4. Create a clickwrap request model
        5. Create a new clickwrap version using SDK
        """
        # Step 1. Create an API client with headers
        api_client = create_click_api_client(
            access_token=args["access_token"]
        )

        # Step 2. Create a display settings model
        display_settings = DisplaySettings(
            consent_button_text="I Agree",
            display_name=f"{args.get('clickwrap_name')} v2",
            downloadable=False,
            format="modal",
            must_read=True,
            must_view=False,
            require_accept=False,
            document_display="document",
            send_to_email=False
        )

        # Read file from a local directory
        # The reads could raise an exception if the file is not available!
        with open(path.join(demo_docs_path, DS_CONFIG["doc_terms_pdf"]),
                  "rb") as file:
            doc_docx_bytes = file.read()
        doc_b64 = base64.b64encode(doc_docx_bytes).decode("ascii")

        # Step 3. Create a document model.
        document = Document(  # Create the DocuSign document object
            document_base64=doc_b64,
            document_name="Terms of Service", # Can be different from actual file name
            file_extension="pdf",  # Many different document types are accepted
            order=0
        )

        # Step 4. Create a clickwrap request model
        clickwrap_request = ClickwrapRequest(
            display_settings=display_settings,
            documents=[document, ],
            name=args.get("clickwrap_name"),
            require_reacceptance=True,
            status="active"
        )

        # Step 5. Create a new clickwrap version using SDK
        accounts_api = AccountsApi(api_client)
        response = accounts_api.create_clickwrap_version(
            account_id=args["account_id"],
            clickwrap_id=args["clickwrap_id"],
            clickwrap_request=clickwrap_request,
        )

        return response

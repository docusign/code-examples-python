from docusign_esign import EnvelopesApi
from flask import request, session

from ...consts import pattern
from ...docusign import create_api_client


class Eg007EnvelopeGetDocController:
    @staticmethod
    def get_args():
        """
        Get session arguments
        """
        # More data validation would be a good idea here
        # Strip anything other than characters listed
        document_id = pattern.sub("", request.form.get("document_id"))

        args = {
            "account_id": session["ds_account_id"],
            "envelope_id": session["envelope_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
            "document_id": document_id,
            "envelope_documents": session["envelope_documents"]
        }
        return args

    @staticmethod
    def worker(args):
        """
        Call the envelope get method
        """
        # Exceptions will be caught by the calling function
        # Step 2 start
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        # Step 2 end        
        # Step 3 start
        envelope_api = EnvelopesApi(api_client)
        document_id = args["document_id"]

        # Call the envelope get method to get the path of the temp file with the documents
        temp_file_path = envelope_api.get_document(
            account_id=args["account_id"],
            document_id=document_id,
            envelope_id=args["envelope_id"]
        )

        # Step 3 end
        
        doc_item = next(item for item in args["envelope_documents"]["documents"] if item["document_id"] == document_id)
        doc_name = doc_item["name"]
        has_pdf_suffix = doc_name[-4:].upper() == ".PDF"
        pdf_file = has_pdf_suffix
        # Add .pdf if it"s a content or summary doc and doesn"t already end in .pdf
        if (doc_item["type"] == "content" or doc_item["type"] == "summary") and not has_pdf_suffix:
            doc_name += ".pdf"
            pdf_file = True
        # Add .zip as appropriate
        if doc_item["type"] == "zip":
            doc_name += ".zip"

        # Return the file information
        if pdf_file:
            mimetype = "application/pdf"
        elif doc_item["type"] == "zip":
            mimetype = "application/zip"
        else:
            mimetype = "application/octet-stream"

        return {"mimetype": mimetype, "doc_name": doc_name, "data": temp_file_path}

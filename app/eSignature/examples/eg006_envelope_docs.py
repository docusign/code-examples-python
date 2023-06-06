from docusign_esign import EnvelopesApi
from flask import session

from ...docusign import create_api_client


class Eg006EnvelopeDocsController:
    @staticmethod
    def get_args():
        """
        Get session arguments
        """
        return {
            "account_id": session["ds_account_id"],
            "envelope_id": session["envelope_id"],
            "base_path": session["ds_base_path"],
            "access_token": session["ds_access_token"],
        }

    @staticmethod
    def worker(args):
        """
        1. Call the EnvelopeDocuments::list method
        """

        #ds-snippet-start:eSign6Step2
        api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
        #ds-snippet-end:eSign6Step2

        #ds-snippet-start:eSign6Step3
        envelope_api = EnvelopesApi(api_client)
        # Call the EnvelopeDocuments::list method
        results = envelope_api.list_documents(account_id=args["account_id"], envelope_id=args["envelope_id"])
        #ds-snippet-end:eSign6Step3

        return results

    @staticmethod
    def save_envelope_documents(results):
        """
            Save the envelopeId and its list of documents in the session so
            they can be used in example 7 (download a document)
        """
        standard_doc_items = [
            {"name": "Combined", "type": "content", "document_id": "combined"},
            {"name": "Zip archive", "type": "zip", "document_id": "archive"},
            {"name": "PDF Portfolio", "type": "content", "document_id": "portfolio"}]
        # The certificate of completion is named "summary".
        # We give it a better name below.
        envelope_doc_items = list(map(lambda doc:
                                      ({"document_id": doc.document_id, "name": "Certificate of completion",
                                        "type": doc.type})
                                      if (doc.document_id == "certificate") else
                                      ({"document_id": doc.document_id, "name": doc.name, "type": doc.type}),
                                      results.envelope_documents))
        envelope_documents = {
            "envelope_id": session["envelope_id"],
            "documents": standard_doc_items + envelope_doc_items  # See https://stackoverflow.com/a/6005217/64904
        }
        session["envelope_documents"] = envelope_documents

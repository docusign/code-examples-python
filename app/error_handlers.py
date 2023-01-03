import json

from flask import render_template
from .api_type import EXAMPLES_API_TYPE


def process_error(err):
    error_body_json = err and hasattr(err, "body") and err.body
    # we can pull the DocuSign error code and message from the response body
    try:
        error_body = json.loads(error_body_json)
    except json.decoder.JSONDecodeError:
        error_body = {}
    error_code = error_body and "errorCode" in error_body and error_body["errorCode"]
    error_message = error_body and "message" in error_body and error_body["message"]

    # Handle error specific for use conditional recipients example (eg34)
    if error_code == "WORKFLOW_UPDATE_RECIPIENTROUTING_NOT_ALLOWED":
        return render_template("eSignature/error_eg34.html")
    
    if EXAMPLES_API_TYPE["Monitor"]:
        if ("(403" in str(err)):
            return render_template("error_enable_monitor.html")

    # In production, may want to provide customized error messages and
    # remediation advice to the user.
    return render_template(
        "error.html",
        err=err,
        error_code=error_code,
        error_message=error_message
    )

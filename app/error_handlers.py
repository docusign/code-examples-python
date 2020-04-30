import json

from flask import render_template


def process_error(err):
    error_body_json = err and hasattr(err, "body") and err.body
    # we can pull the DocuSign error code and message from the response body
    error_body = json.loads(error_body_json)
    error_code = error_body and "errorCode" in error_body and error_body["errorCode"]
    error_message = error_body and "message" in error_body and error_body["message"]
    # In production, may want to provide customized error messages and
    # remediation advice to the user.
    return render_template(
        "error.html",
        err=err,
        error_code=error_code,
        error_message=error_message
    )

from flask import request
import hmac
import hashlib
import base64

class Eg001ValidateWebhookMessageController:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "secret": request.form.get("secret"),
            "payload": request.form.get("payload"),
        }

    @staticmethod
    def worker(args):
        """
        1. Create an API client with headers
        2. Get your monitor data via SDK
        """        
        #ds-snippet-start:Connect1Step1
        key = bytes(args['secret'], 'utf-8')
        payload = bytes(args['payload'], 'utf-8')

        hmac_hash = hmac.new(key, payload, hashlib.sha256)
        result = base64.b64encode(hmac_hash.digest()).decode('utf-8')
        #ds-snippet-end:Connect1Step1

        return result

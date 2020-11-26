from flask import session


class Eg003Controller:
    @staticmethod
    def get_args():
        """Get required session and request arguments"""
        return {
            "account_id": session["ds_account_id"],  # Represents your {ACCOUNT_ID}
            "access_token": session["ds_access_token"],  # Represents your {ACCESS_TOKEN}
            "clickwrap_id": session["clickwrap_id"],
            "clickwrap_is_active": session["clickwrap_is_active"]
        }

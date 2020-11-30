from flask import session


class Eg004Controller:
    @staticmethod
    def get_args():
        """Get required session arguments"""
        return {
            "account_id": session.get("ds_account_id"),  # Represents your {ACCOUNT_ID}
            "access_token": session.get("ds_access_token"),  # Represents your {ACCESS_TOKEN}
            "clickwrap_id": session.get("clickwrap_id"),
            "clickwrap_is_active": session.get("clickwrap_is_active")
        }

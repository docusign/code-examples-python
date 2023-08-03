import datetime
import unittest

from app.click.examples.eg001_create_clickwrap import Eg001CreateClickwrapController
from app.click.examples.eg002_activate_clickwrap import Eg002ActivateClickwrapController
from .test_helper import TestHelper, CONFIG, ApiType


class ClickTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        results = TestHelper.authenticate([ApiType.CLICK.value])

        cls.access_token = results["access_token"]
        cls.account_id = results["account_id"]
        cls.base_path = results["base_path"]

    def test_create_clickwrap_worker(self):
        args = {
            "account_id": self.account_id,
            "access_token": self.access_token,
            "clickwrap_name": f"{CONFIG['clickwrap_name']}_{int(datetime.datetime.utcnow().timestamp())}"
        }

        results = Eg001CreateClickwrapController.worker(args)

        self.assertIsNotNone(results)
        self.assertIsNotNone(results.clickwrap_id)

    def test_activate_clickwrap_worker(self):
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "statuses": ["inactive", "draft"]
        }
        results = Eg002ActivateClickwrapController.get_inactive_clickwraps(args)
        clickwrap = results["clickwraps"][0]

        clickwrap_args = f"{{\"clickwrap_id\": \"{clickwrap.clickwrap_id}\",\"version_number\": \"{clickwrap.version_number}\"}}"
        args["clickwrap"] = clickwrap_args

        results = Eg002ActivateClickwrapController.worker(args)

        self.assertIsNotNone(results)
        self.assertEqual(results.status, "active")

    def test_activate_clickwrap_get_inactive_clickwraps(self):
        args = {
            "account_id": self.account_id,
            "base_path": self.base_path,
            "access_token": self.access_token,
            "statuses": ["inactive", "draft"]
        }

        results = Eg002ActivateClickwrapController.get_inactive_clickwraps(args)

        self.assertIsNotNone(results)


if __name__ == '__main__':
    unittest.main()

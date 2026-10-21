import json
import unittest
from unittest.mock import patch

from scripts.setup_free_scheduler import build_job, safe_preview, main


class FreeSchedulerTests(unittest.TestCase):
    def test_trigger_prepares_twenty_minutes_before_pakistan_target(self):
        job = build_job("dummy-token", "15:00", "Asia/Karachi")
        self.assertEqual(job["schedule"]["timezone"], "Asia/Karachi")
        self.assertEqual(job["schedule"]["hours"], [14])
        self.assertEqual(job["schedule"]["minutes"], [40])
        self.assertEqual(job["requestMethod"], 1)
        self.assertTrue(json.loads(job["extendedData"]["body"])["inputs"]["scheduled"])

    def test_preview_never_contains_the_private_token(self):
        token = "private-example-token-do-not-print"
        preview = json.dumps(safe_preview(build_job(token, "12:15", "Asia/Karachi")))
        self.assertNotIn(token, preview)
        self.assertNotIn("Bearer", preview)
        self.assertIn("Authorization", preview)

    def test_setup_rejects_a_git_login_token_before_any_network_call(self):
        with patch("scripts.setup_free_scheduler.dotenv_values", return_value={
            "GITHUB_DISPATCH_TOKEN": "gho_do-not-export-existing-login",
            "CRONJOB_API_KEY": "private-test-key",
        }), patch.dict("os.environ", {"GITHUB_DISPATCH_TOKEN": "", "CRONJOB_API_KEY": ""}), \
             patch("sys.argv", ["setup_free_scheduler.py", "--apply"]), \
             patch("scripts.setup_free_scheduler.requests.get") as get, \
             patch("builtins.print"):
            with self.assertRaisesRegex(RuntimeError, "fine-grained"):
                main()
            get.assert_not_called()

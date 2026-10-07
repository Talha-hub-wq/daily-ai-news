"""Deployment checks without contacting news services or sending email."""
import datetime
import unittest
from unittest.mock import patch

import pytz
import schedule

from app import main
from app.llm_provider import OllamaProvider
from app.scheduler import NewsScheduler


class DeploymentTests(unittest.TestCase):
    def test_pakistan_schedule_resolves_to_1700_utc(self):
        scheduler = NewsScheduler()
        scheduler.schedule_daily("22:00", lambda: None)
        job = scheduler.scheduled_jobs[0]
        try:
            local = job.at_time_zone.localize(datetime.datetime.combine(
                datetime.date(2026, 10, 7), job.at_time))
            self.assertEqual(local.astimezone(pytz.UTC).strftime("%H:%M"), "17:00")
        finally:
            schedule.cancel_job(job)

    def test_webhook_and_logs_require_token(self):
        client = main.app.test_client()
        with patch.object(main, "TRIGGER_TOKEN", "private-test-token"), \
             patch.object(main, "send_daily_news", return_value=True) as send:
            for header in [None, "Bearer wrong", "Bearer \u00e9"]:
                headers = {"Authorization": header} if header else {}
                self.assertEqual(client.post("/trigger-news", headers=headers).status_code, 401)
                self.assertEqual(client.get("/logs", headers=headers).status_code, 401)
            send.assert_not_called()
            response = client.post("/trigger-news", headers={
                "Authorization": "Bearer private-test-token"})
            self.assertEqual(response.status_code, 200)
            send.assert_called_once()
        with patch.object(main, "TRIGGER_TOKEN", ""):
            self.assertEqual(client.post("/trigger-news").status_code, 401)

    def test_failed_one_shot_exits_nonzero(self):
        with patch.object(main, "validate_config"), \
             patch.object(main, "send_daily_news", return_value=False), \
             patch.object(main.sys, "argv", ["main.py", "--run-once"]):
            with self.assertRaises(SystemExit) as result:
                main.main()
            self.assertEqual(result.exception.code, 1)

    def test_readiness_cli_does_not_send_email(self):
        with patch.object(main, "validate_config"), \
             patch.object(main, "NewsSummarizer") as summarizer, \
             patch.object(main, "send_daily_news") as send, \
             patch.object(main.sys, "argv", ["main.py", "--check-services"]):
            main.main()
            summarizer.return_value.check_ready.assert_called_once()
            send.assert_not_called()

    @patch("app.llm_provider.requests.get")
    def test_model_readiness_and_proxy_auth(self, get):
        provider = OllamaProvider("https://example.test", "qwen3:8b", api_token="test-token")
        get.return_value.json.return_value = {"models": [{"name": "qwen3:8b"}]}
        self.assertTrue(provider.check_ready())
        self.assertEqual(get.call_args.kwargs["headers"], {"Authorization": "Bearer test-token"})
        for body in [{}, [], {"models": None}, {"models": [{"name": "other"}]}]:
            get.return_value.json.return_value = body
            with self.subTest(body=body), self.assertRaises(ValueError):
                provider.check_ready()

    def test_unavailable_llm_stops_pipeline_before_news_or_email(self):
        with patch.object(main, "NewsSummarizer") as summarizer, \
             patch.object(main, "NewsFetcher") as fetcher, \
             patch.object(main, "EmailSender") as sender, \
             patch.object(main, "logger"):
            summarizer.return_value.check_ready.side_effect = ConnectionError("unavailable")
            self.assertFalse(main.send_daily_news())
            fetcher.assert_not_called()
            sender.assert_not_called()

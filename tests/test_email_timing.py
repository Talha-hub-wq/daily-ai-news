"""Email dates must identify the actual Pakistan calendar day."""
import unittest
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from unittest.mock import patch

from app.email_sender import EmailSender


class EmailTimingTests(unittest.TestCase):
    def test_headers_and_body_use_pakistan_date_across_utc_midnight(self):
        sender = EmailSender("sender@example.test", "dummy", "smtp.example.test", 587)
        template = Path(__file__).resolve().parents[1] / "templates" / "email_template.html"
        with patch("app.email_sender.datetime") as clock, \
             patch("app.email_sender.SCHEDULE_TIMEZONE", "Asia/Karachi"), \
             patch.object(sender, "_send_smtp") as smtp:
            clock.now.return_value = datetime(2026, 10, 19, 20, 15, tzinfo=timezone.utc)
            self.assertTrue(sender.send_news_email("recipient@example.test", [], [], html_template=str(template)))
        message = smtp.call_args.args[1]
        self.assertIn("2026-10-20", message["Subject"])
        date = parsedate_to_datetime(message["Date"])
        self.assertEqual(date.utcoffset(), timedelta(hours=5))
        self.assertEqual((date.day, date.hour, date.minute), (20, 1, 15))
        self.assertEqual(message["X-Digest-Timezone"], "Asia/Karachi")
        self.assertTrue(message["Message-ID"])
        html = message.get_payload()[0].get_payload(decode=True).decode("utf-8")
        self.assertIn("Digest date: 2026-10-20", html)
        self.assertNotIn("{{ GENERATED_AT }}", html)

    def test_different_days_have_different_subjects(self):
        sender = EmailSender("sender@example.test", "dummy", "smtp.example.test", 587)
        template = Path(__file__).resolve().parents[1] / "templates" / "email_template.html"
        with patch("app.email_sender.datetime") as clock, patch.object(sender, "_send_smtp") as smtp:
            for day in (18, 19):
                clock.now.return_value = datetime(2026, 10, day, 17, tzinfo=timezone.utc)
                self.assertTrue(sender.send_news_email("recipient@example.test", [], [], html_template=str(template)))
        first, second = (call.args[1] for call in smtp.call_args_list)
        self.assertNotEqual(first["Subject"], second["Subject"])
        self.assertNotEqual(first["Message-ID"], second["Message-ID"])

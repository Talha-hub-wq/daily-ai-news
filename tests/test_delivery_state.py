import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.delivery_state import DeliveryState


class DeliveryStateTests(unittest.TestCase):
    def test_new_day_can_send_and_sent_day_is_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            state = DeliveryState(path, "2026-10-21")
            self.assertTrue(state.can_send())
            state.mark("sent")
            self.assertFalse(DeliveryState(path, "2026-10-21").can_send())
            self.assertTrue(DeliveryState(path, "2026-10-22").can_send())

    def test_ambiguous_smtp_attempt_cannot_be_blindly_retried(self):
        with tempfile.TemporaryDirectory() as directory:
            state = DeliveryState(Path(directory) / "state.json", "2026-10-21")
            state.mark("submitting")
            with self.assertRaisesRegex(RuntimeError, "uncertain"):
                state.can_send()

    def test_saved_delivery_skips_pipeline_without_fetching_or_sending(self):
        from app import main
        from datetime import datetime, timezone
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            now = datetime.now(timezone.utc).astimezone(__import__('pytz').timezone(main.SCHEDULE_TIMEZONE))
            DeliveryState(path, now.date(), main.SCHEDULE_TIME).mark("sent")
            with patch.object(main, "NewsFetcher") as fetcher, patch.object(main, "EmailSender") as sender:
                self.assertTrue(main.send_daily_news(delivery_state_path=str(path)))
            fetcher.assert_not_called()
            sender.assert_not_called()

    def test_changing_target_time_does_not_suppress_the_new_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            DeliveryState(path, "2026-10-21", "11:40").mark("sent")
            new_slot = DeliveryState(path, "2026-10-21", "12:15")
            self.assertTrue(new_slot.can_send())
            new_slot.mark("sent")
            self.assertFalse(DeliveryState(path, "2026-10-21", "12:15").can_send())

    def test_slot_keys_are_distinct_and_stable_for_retries(self):
        from app.delivery_time import delivery_identity
        first = delivery_identity("2026-10-21", "11:40")
        second = delivery_identity("2026-10-21", "12:15")
        self.assertNotEqual(first["cache_key"], second["cache_key"])
        self.assertNotEqual(first["state_path"], second["state_path"])
        self.assertEqual(second, delivery_identity("2026-10-21", "12:15"))

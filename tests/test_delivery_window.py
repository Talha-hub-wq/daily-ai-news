import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

from app.delivery_time import scheduled_delivery_target, wait_until_delivery


class DeliveryWindowTests(unittest.TestCase):
    def test_scheduled_cli_refuses_expired_run_before_fetching(self):
        from app import main
        with patch.object(main, "validate_config"), \
             patch.object(main, "scheduled_delivery_target", side_effect=RuntimeError("late")), \
             patch.object(main, "send_daily_news") as pipeline, patch.object(main, "logger"), \
             patch.object(main.sys, "argv", ["main.py", "--run-once", "--scheduled"]):
            with self.assertRaises(SystemExit) as result:
                main.main()
            self.assertEqual(result.exception.code, 1)
            pipeline.assert_not_called()

    def test_preparation_targets_ten_pm_in_pakistan(self):
        now = datetime(2026, 10, 19, 16, 45, tzinfo=timezone.utc)
        target = scheduled_delivery_target("22:00", "Asia/Karachi", now)
        self.assertEqual(target.astimezone(timezone.utc).hour, 17)
        self.assertEqual(target.day, 19)

    def test_late_or_next_day_schedule_cannot_send_stale_digest(self):
        for hour in (15, 20):
            now = datetime(2026, 10, 19, hour, 1, tzinfo=timezone.utc)
            with self.subTest(hour=hour), self.assertRaises(RuntimeError):
                scheduled_delivery_target("22:00", "Asia/Karachi", now)

    def test_small_scheduler_delay_can_deliver_same_evening(self):
        now = datetime(2026, 10, 19, 17, 15, tzinfo=timezone.utc)
        target = scheduled_delivery_target("22:00", "Asia/Karachi", now)
        wait_until_delivery(target, clock=lambda: now, sleep=Mock())

    def test_three_hour_delay_is_caught_up_instead_of_losing_the_email(self):
        now = datetime(2026, 10, 21, 10, 15, tzinfo=timezone.utc)
        target = scheduled_delivery_target("12:15", "Asia/Karachi", now)
        self.assertEqual((target.hour, target.minute), (12, 15))
        wait_until_delivery(target, clock=lambda: now, sleep=Mock())

    def test_afternoon_target_is_0715_utc(self):
        now = datetime(2026, 10, 21, 7, 0, tzinfo=timezone.utc)
        target = scheduled_delivery_target("12:15", "Asia/Karachi", now)
        self.assertEqual(target.astimezone(timezone.utc).strftime("%H:%M"), "07:15")

    def test_waits_until_target_without_sending_early(self):
        target = datetime(2026, 10, 19, 17, tzinfo=timezone.utc)
        now = [target - timedelta(seconds=45)]
        def advance(seconds):
            now[0] += timedelta(seconds=seconds)
        sleep = Mock(side_effect=advance)
        wait_until_delivery(target, clock=lambda: now[0], sleep=sleep)
        self.assertEqual(now[0], target)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [30, 15])

    def test_slow_preparation_cannot_roll_into_next_day(self):
        import pytz
        target = datetime(2026, 10, 19, 17, tzinfo=timezone.utc).astimezone(pytz.timezone("Asia/Karachi"))
        with self.assertRaises(RuntimeError):
            wait_until_delivery(target, clock=lambda: target + timedelta(hours=3))

    def test_expired_digest_does_not_reach_smtp(self):
        from app import main
        with patch.object(main, "NewsSummarizer"), \
             patch.object(main, "NewsFetcher") as fetcher, \
             patch.object(main, "get_hackernews_tech_stories", return_value=[]), \
             patch.object(main, "get_nitter_tweets", return_value=[]), \
             patch.object(main, "wait_until_delivery", side_effect=RuntimeError("expired")), \
             patch.object(main, "EmailSender") as sender, patch.object(main, "logger"):
            fetcher.return_value.fetch_ai_news.return_value = [{"title": "AI news"}]
            fetcher.return_value.fetch_world_news.return_value = []
            self.assertFalse(main.send_daily_news(delivery_target=Mock()))
            sender.assert_not_called()

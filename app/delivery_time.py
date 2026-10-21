"""Plan local-day delivery, including catch-up after a delayed scheduler start."""
import time
from datetime import datetime, time as time_of_day, timedelta, timezone

import pytz


PREPARATION_WINDOW = timedelta(minutes=30)


def delivery_identity(digest_date, schedule_time):
    """A time change is a new delivery slot; retries of that slot share its ledger."""
    day = str(digest_date)
    datetime.strptime(day, "%Y-%m-%d")
    slot = datetime.strptime(schedule_time, "%H:%M").strftime("%H%M")
    return {"date": day, "slot": slot,
            "state_path": f".delivery-state/{day}-{slot}.json",
            "cache_key": f"news-delivery-v2-{day}-{slot}"}


def scheduled_delivery_target(time_str, timezone_name, now=None):
    """Permit preparation shortly before the target and catch-up on the same local day."""
    now = now if now is not None else datetime.now(timezone.utc)
    zone = pytz.timezone(timezone_name)
    local_now = now.astimezone(zone)
    hour, minute = map(int, time_str.split(":"))
    target = zone.localize(datetime.combine(local_now.date(), time_of_day(hour, minute)))
    if local_now < target - PREPARATION_WINDOW:
        raise RuntimeError("Daily delivery is not due yet")
    return target


def wait_until_delivery(target, clock=None, sleep=None):
    """Wait for the chosen target without rolling it into a different calendar day."""
    clock = clock if clock is not None else lambda: datetime.now(timezone.utc)
    sleep = sleep if sleep is not None else time.sleep
    while True:
        now = clock()
        if now.astimezone(target.tzinfo).date() != target.date():
            raise RuntimeError("Digest preparation crossed its local calendar day; email not sent")
        remaining = (target - now).total_seconds()
        if remaining <= 0:
            return
        sleep(min(remaining, 30))

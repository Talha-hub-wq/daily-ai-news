"""Keep scheduled delivery on the intended local evening."""
import time
from datetime import datetime, time as time_of_day, timedelta, timezone

import pytz


PREPARATION_WINDOW = timedelta(minutes=30)
MAX_LATENESS = timedelta(minutes=60)


def scheduled_delivery_target(time_str, timezone_name, now=None):
    """Permit preparation shortly before the target, or delivery up to one hour late."""
    now = now if now is not None else datetime.now(timezone.utc)
    zone = pytz.timezone(timezone_name)
    local_now = now.astimezone(zone)
    hour, minute = map(int, time_str.split(":"))
    target = zone.localize(datetime.combine(local_now.date(), time_of_day(hour, minute)))
    if not target - PREPARATION_WINDOW <= local_now <= target + MAX_LATENESS:
        raise RuntimeError("Scheduled run is outside the delivery window; refusing a stale digest")
    return target


def wait_until_delivery(target, clock=None, sleep=None):
    """Wait for the chosen target without rolling it into a different calendar day."""
    clock = clock if clock is not None else lambda: datetime.now(timezone.utc)
    sleep = sleep if sleep is not None else time.sleep
    while True:
        now = clock()
        if now > target + MAX_LATENESS:
            raise RuntimeError("Digest preparation exceeded the delivery window; email not sent")
        remaining = (target - now).total_seconds()
        if remaining <= 0:
            return
        sleep(min(remaining, 30))

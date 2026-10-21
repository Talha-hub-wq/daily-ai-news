"""Small credential-free ledger persisted by the workflow between daily checks."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path


class DeliveryState:
    def __init__(self, path, digest_date, schedule_time=None):
        self.path = Path(path)
        self.digest_date = str(digest_date)
        self.schedule_time = schedule_time

    def status(self):
        if not self.path.exists():
            return None
        record = json.loads(self.path.read_text(encoding="utf-8"))
        if record.get("date") != self.digest_date:
            return None
        if self.schedule_time is not None and record.get("schedule_time") != self.schedule_time:
            return None
        status = record.get("status")
        if status not in {"submitting", "sent"}:
            raise ValueError("Invalid delivery ledger; inspect before retrying")
        return status

    def can_send(self):
        status = self.status()
        if status == "submitting":
            raise RuntimeError("Previous SMTP result is uncertain; inspect inbox before retrying")
        return status != "sent"

    def mark(self, status):
        if status not in {"submitting", "sent"}:
            raise ValueError("Invalid delivery status")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {"date": self.digest_date, "status": status,
                  "schedule_time": self.schedule_time,
                  "updated_at": datetime.now(timezone.utc).isoformat(),
                  "run_id": os.getenv("GITHUB_RUN_ID")}
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(record), encoding="utf-8")
        temporary.replace(self.path)

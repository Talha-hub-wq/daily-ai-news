"""Preview or configure a cron-job.org trigger using privately supplied scoped keys."""
import argparse
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import sys

import requests
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from config.settings import SCHEDULE_TIME, SCHEDULE_TIMEZONE

WORKFLOW_URL = "https://api.github.com/repos/Talha-hub-wq/daily-ai-news/actions/workflows/daily-news.yml"
CRON_API = "https://api.cron-job.org"


def build_job(dispatch_token, target=SCHEDULE_TIME, timezone_name=SCHEDULE_TIMEZONE):
    trigger = datetime.strptime(target, "%H:%M") - timedelta(minutes=20)
    return {
        "title": f"Daily AI news - {target} {timezone_name}",
        "enabled": True,
        "url": WORKFLOW_URL + "/dispatches",
        "requestMethod": 1,
        "requestTimeout": 30,
        "saveResponses": False,
        "schedule": {"timezone": timezone_name, "expiresAt": 0,
                     "hours": [trigger.hour], "minutes": [trigger.minute],
                     "mdays": [-1], "months": [-1], "wdays": [-1]},
        "extendedData": {
            "headers": {"Authorization": "Bearer " + dispatch_token,
                        "Accept": "application/vnd.github+json",
                        "Content-Type": "application/json",
                        "X-GitHub-Api-Version": "2022-11-28"},
            "body": json.dumps({"ref": "main", "inputs": {"scheduled": "true"}}),
        },
    }


def safe_preview(job):
    return {"title": job["title"], "url": job["url"], "method": "POST",
            "schedule": job["schedule"],
            "header_names": sorted(job["extendedData"]["headers"]),
            "body": json.loads(job["extendedData"]["body"])}


def cron_request(api_key, method, path, payload=None):
    response = requests.request(
        method, CRON_API + path,
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        json=payload, timeout=30, allow_redirects=False,
    )
    if response.status_code not in (200, 201):
        raise RuntimeError(f"cron-job.org returned HTTP {response.status_code}")
    return response.json()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create/update the external cron job")
    parser.add_argument("--job-id", type=int, help="Existing job to update after a time change")
    args = parser.parse_args()
    values = dotenv_values(ROOT / ".env")
    dispatch_token = os.getenv("GITHUB_DISPATCH_TOKEN") or values.get("GITHUB_DISPATCH_TOKEN")
    api_key = os.getenv("CRONJOB_API_KEY") or values.get("CRONJOB_API_KEY")
    job = build_job(dispatch_token or "not-configured")
    print(json.dumps(safe_preview(job), indent=2))
    if not args.apply:
        print("Preview only; no external changes made")
        return
    if not dispatch_token or not api_key:
        raise RuntimeError("Set CRONJOB_API_KEY and a repo-scoped GITHUB_DISPATCH_TOKEN privately in .env")
    if not dispatch_token.startswith("github_pat_"):
        raise RuntimeError("Use a new fine-grained GitHub token; do not reuse a Git login or classic token")
    # Check the supplied token against the intended repository before storing it externally.
    response = requests.get(WORKFLOW_URL, headers={
        "Authorization": "Bearer " + dispatch_token,
        "Accept": "application/vnd.github+json", "User-Agent": "daily-ai-news-setup",
    }, timeout=30, allow_redirects=False)
    if response.status_code != 200:
        raise RuntimeError(f"GitHub token cannot access the intended workflow (HTTP {response.status_code})")
    job_id = args.job_id
    if job_id is None:
        listing = cron_request(api_key, "GET", "/jobs")
        if listing.get("someFailed"):
            raise RuntimeError("Cron job list is incomplete; retry before creating a job")
        matches = [item for item in listing.get("jobs", []) if item.get("title") == job["title"]]
        if len(matches) > 1:
            raise RuntimeError("Multiple matching jobs; select the correct --job-id")
        if matches:
            job_id = matches[0]["jobId"]
    if job_id is not None:
        previous = cron_request(api_key, "GET", f"/jobs/{job_id}")["jobDetails"]
        if previous.get("url") != job["url"]:
            raise RuntimeError("Refusing to modify a job that targets another endpoint")
        cron_request(api_key, "PATCH", f"/jobs/{job_id}", {"job": job})
    else:
        job_id = cron_request(api_key, "PUT", "/jobs", {"job": job})["jobId"]
    detail = cron_request(api_key, "GET", f"/jobs/{job_id}")["jobDetails"]
    if not detail.get("enabled") or detail.get("schedule") != job["schedule"]:
        raise RuntimeError("Created job settings could not be verified in cron-job.org")
    print(f"External scheduler configured and verified; job ID: {job_id}")
    print("This verifies the trigger configuration, not a future email delivery. Test it in the console.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, requests.RequestException, ValueError, KeyError) as error:
        if isinstance(error, RuntimeError):
            print(str(error), file=sys.stderr)
        else:
            print(f"Setup failed ({type(error).__name__}); no private response data displayed", file=sys.stderr)
        sys.exit(1)

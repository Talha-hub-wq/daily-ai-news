# Free external scheduler for the 12:15 PM Pakistan digest

The email pipeline works when dispatched, but GitHub's built-in cron has started jobs hours late. An external trigger avoids relying on that cron event. The application still enforces the configured Pakistan send time and prevents repeated submissions of the same date/time slot.

## 1. Create the free scheduler account

Open [cron-job.org Console](https://console.cron-job.org/), create a free account, verify your email, and sign in. In **Settings**, generate an API key. Keep it private.

This computer session has no controllable browser, so account creation/sign-in must be completed by you. No cron-job.org job has been created yet.

## 2. Create a restricted GitHub dispatch token

Open [GitHub fine-grained tokens](https://github.com/settings/personal-access-tokens/new).

1. Give the token a recognizable name, such as `daily-news-scheduler`.
2. Choose resource owner `Talha-hub-wq` and only repository `daily-ai-news`.
3. Set repository permission **Actions: Read and write**. Metadata read is included automatically. No contents, administration or other repository permissions are needed.
4. Choose an expiry date and record it so the token can be rotated before expiry interrupts scheduling.
5. Generate the token. Keep it private; do not paste it into chat.

The existing Git credential used for development has administrator access and must not be copied to cron-job.org. Use this newly restricted token instead.

## 3. Put the two keys in the existing private local `.env`

Add these two entries without altering your news/email credentials:

```dotenv
CRONJOB_API_KEY=your_cron_job_org_api_key
GITHUB_DISPATCH_TOKEN=your_new_repo_scoped_github_token
```

The setup command will use the first key only to manage the cron-job.org job. It will store the second key in that job's private Authorization header so the service can start this repository's workflow. NewsAPI and SMTP secrets stay in GitHub Actions; they are not sent to cron-job.org.

## 4. Preview the exact job

```powershell
Set-Location 'D:\daily AI news'
.\venv\Scripts\python.exe scripts/setup_free_scheduler.py
```

This makes no external changes and prints no token values. With the current `12:15` target, the preview schedules a daily trigger at **11:55 AM Asia/Karachi**. The cloud job then prepares news and waits until **12:15 PM** before SMTP submission.

## 5. Create and verify the job

After approving storage of the restricted dispatch token at cron-job.org:

```powershell
.\venv\Scripts\python.exe scripts/setup_free_scheduler.py --apply
```

The script checks the GitHub workflow token, creates or updates the matching job, and reads its settings back. It uses the fixed GitHub repository/workflow endpoint, POST method, and this request body:

```json
{"ref":"main","inputs":{"scheduled":"true"}}
```

If the schedule later changes, pass the existing job ID to update that exact job rather than leaving the old trigger active:

```powershell
.\venv\Scripts\python.exe scripts/setup_free_scheduler.py --apply --job-id YOUR_JOB_ID
```

The GitHub fifteen-minute cron checks can remain as best-effort fallback. The saved date/time-slot ledger normally prevents duplicate email when both clocks dispatch the same slot.

## 6. Verify the trigger and email separately

Use the scheduler console's test/run control. It should receive GitHub HTTP **204**, meaning the workflow was accepted. Then inspect GitHub Actions for the new `workflow_dispatch` run, its SMTP result and actual Pakistan timestamp. Finally confirm inbox receipt. A successful cron HTTP request alone does not prove that news generation or email delivery succeeded.

When testing before 11:45 AM, scheduled mode correctly skips because preparation is not due. When the current date/time slot is already sent, it correctly skips a duplicate. Monitor the first actual 11:55 AM cron event and 12:15 PM send; manual testing is not proof of a future scheduled event.

This improves the clock used to start the job. It does not guarantee exact inbox arrival, uninterrupted GitHub runner availability, or atomic exactly-once SMTP delivery.

Reference: [cron-job.org API](https://docs.cron-job.org/rest-api.html), [GitHub workflow dispatch](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event).

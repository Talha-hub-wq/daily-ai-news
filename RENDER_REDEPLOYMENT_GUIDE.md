# Free deployment: daily AI news while your PC is off

## Current delivery target: 12:15 PM Pakistan time

The daily target has been changed from 11:40 AM to **12:15 PM Asia/Karachi** (07:15 UTC). Frequent checks, same-day recovery and the per-day delivery ledger remain enabled. The October 21 timed test described below actually ran at 11:40 AM and remains historical evidence; it does not describe the new target.


## October 21 correction ? 11:40 AM Pakistan test

The October 19?20 scheduled runs started more than three hours late. Their logs show that the previous one-hour delivery cutoff rejected them before collecting news or sending mail. That cutoff is removed. The current target is **11:40 AM Asia/Karachi** (06:40 UTC), with frequent checks every 15 minutes instead of a single daily trigger. Delayed checks catch up on the same local day; the daily cached delivery ledger prevents ordinary repeated submissions. Preparation failures before SMTP can be retried by the next check. If SMTP acceptance is uncertain, the saved `submitting` record blocks blind retries and requires inbox/log inspection. Cache loss or a runner crash before persistence remains a limitation; SMTP does not provide an atomic exactly-once transaction with Actions cache.

The workflow's `scheduled` manual-dispatch input exercises the same 11:40 timing gate. No OpenAI provider or paid service is introduced. GitHub cron itself still has no exact-time guarantee; a persistent/reliable external scheduler would be needed for a stronger timing commitment. Earlier 10 PM/one-hour-cutoff descriptions below are historical and superseded by this correction.


Updated October 19, 2026. Branch: `ollama-with-AI-News-Agent`.

## October 19 diagnosis and correction

The production default branch still used the old `25 13 * * *` schedule (6:25 PM Pakistan time) and called the Render endpoint. The replacement draft PR had never been merged; GitHub Actions had no sending credentials. Daily runs from October 7?17 failed. The October 18 run finished at **21:43:56 Pakistan time**, matching the screenshot's 9:43 PM message. These records establish missed runs and variable start times; they do not establish that Gmail queued a message for 3?4 days. Original email Received headers would be needed to prove mail-server delivery latency.

After explicit user approval on October 19, the four private news/email values were encrypted into repository Actions secrets and both old keep-alive workflows were disabled. [The first real cloud email test succeeded](https://github.com/Talha-hub-wq/daily-ai-news/actions/runs/39234426654). This verifies runner setup, Ollama, collection, summarization and SMTP submission; inbox receipt remains a recipient-side check.

The timing correction starts preparation at **21:45 Pakistan time** (`45 16 * * *` UTC), then `--scheduled` holds SMTP delivery until **22:00 Pakistan time**. Scheduled mode allows up to **23:00** for scheduler/processing delay. Outside that window it fails visibly and sends no stale next-day digest. Manual tests send immediately. A missed/out-of-window job is not automatically replayed later.

Email subjects now include the Pakistan digest date, and each message has explicit Date, Message-ID and generation-time fields. The unused Twitter list is no longer fetched/summarized before email, reducing avoidable work.

GitHub's free scheduler still provides no exact-start guarantee. Starting preparation earlier absorbs modest queue/processing delays, but cannot guarantee a daily 22:00 inbox receipt or eliminate platform outages. Watch Actions failures and the first scheduled run.

## The selected setup

You confirmed that you use the free tier and need delivery while your PC is off. The setup is therefore:

```text
GitHub preparation: 16:45 UTC / 9:45 PM Pakistan time
    -> standard GitHub-hosted Ubuntu runner
    -> install Ollama and pull qwen3:1.7b
    -> fetch articles, summarize, wait until 10 PM Pakistan time, send via SMTP
    -> runner exits

Render Free web service -> public status endpoint (allowed to sleep)
```

The daily email job does not call Render, so Render sleeping does not stop delivery. Ollama runs on the GitHub cloud runner, not your PC. No tunnel or paid model API is needed. Your local `.env` still uses `qwen3:8b`; the workflow selects `qwen3:1.7b` to reduce CPU inference requirements. The smaller model can produce different summaries. Its end-to-end performance on GitHub still needs a real test.

Standard GitHub-hosted runners are free for public repositories. Your repository was public when checked; private repositories have a free allowance and different billing rules. This workflow uses a standard runner, not a paid larger runner. [GitHub billing](https://docs.github.com/en/actions/concepts/billing-and-usage).

GitHub schedules may start late, and a digest needs additional time to download the model, fetch and summarize news. This is a 9:45 PM preparation start with a 10 PM send target, not guaranteed inbox receipt at exactly 10 PM. Public repository schedules can be disabled after 60 days of inactivity. [GitHub schedule rules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

Free Render blocks outbound SMTP ports 25, 465 and 587, and does not offer free Cron Jobs. That is why the existing SMTP pipeline runs on GitHub instead of inside free Render. [Render free limitations](https://render.com/docs/free).

## What was checked in the existing deployment

- [Existing web service](https://daily-ai-news-merl.onrender.com/) responded HTTP 200 after waking. Its response advertised the old `13:25 (server local time)` schedule. This establishes startup/liveness only.
- Available remote logs showed startup entries, not verified recent email delivery.
- The latest five available daily GitHub runs, June 12?16, failed. [Latest daily run](https://github.com/Talha-hub-wq/daily-ai-news/actions/runs/27638226768).
- The old YAML used `25 13 * * *`, which means 6:25 PM Pakistan time, not 10 PM. There were duplicate scheduled keep-alive workflows.
- The remote repository's last push was May 7 and only `main` was published when inspected.
- Publishing the prepared branch failed: GitHub returned HTTP 403 stating that **the repository is archived and read-only**. The repository was subsequently unarchived and the feature branch published; see live progress above. No Render deployment has happened yet.

The new workflow and free Render Blueprint are prepared locally. The earlier paid Cron proposal has been replaced; no paid resource was created.

## Step 1 ? unarchive the repository

1. Sign into the GitHub account with owner/admin rights for `Talha-hub-wq/daily-ai-news`.
2. Open repository **Settings ? General ? Danger Zone ? Unarchive this repository**.
3. Follow GitHub's confirmation. This changes repository availability; it does not deploy the local branch.
4. Check Actions settings allow GitHub Actions and the official checkout/setup-python actions.

An archived repository must be unarchived before it accepts changes. If you cannot unarchive it, use a new repository you control and connect that repository to Render instead. [GitHub archiving instructions](https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories).

## Step 2 ? publish the feature branch

The deployment changes are committed locally on the feature branch. Review any further working-tree edits before staging them. Keep `.env`, logs and virtual environments out of Git.

```powershell
Set-Location 'D:\daily AI news'
git branch --show-current
git status --short
# After committing reviewed changes:
git push -u origin ollama-with-AI-News-Agent
```

The active branch should be `ollama-with-AI-News-Agent`. Publishing that branch leaves `main` unchanged.

## Step 3 ? add GitHub Actions secrets

Open repository **Settings ? Secrets and variables ? Actions ? Secrets ? New repository secret**. Add these four values privately:

| Secret | What to enter |
|---|---|
| `NEWSAPI_KEY` | Existing NewsAPI credential |
| `EMAIL_SENDER` | SMTP login/from address |
| `EMAIL_PASSWORD` | SMTP credential; for Gmail, use an app password where required |
| `EMAIL_RECIPIENT` | Your destination inbox |

GitHub does not receive your local `.env` automatically. Use your existing private configuration to populate these settings; do not paste passwords into source files or chat.

Optional **Variables** under the same Actions settings:

| Variable | Default / purpose |
|---|---|
| `CLOUD_LLM_MODEL` | `qwen3:1.7b`; override only with a model suitable for the runner |
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587`; sender currently uses STARTTLS |
| `DAILY_NEWS_SCHEDULER` | Unset enables scheduling; set `disabled` to pause scheduled sends |
| `RENDER_SERVICE_URL` | Existing Render HTTPS URL; used only by the optional manual health check |

No OpenAI key, hosted Ollama endpoint, `LLM_API_TOKEN` or `TRIGGER_TOKEN` is needed for the cloud email job. Do not change the repository's public/private setting merely to set up this deployment.

## Step 4 ? test the new workflow on the feature branch

1. Open **Actions ? Daily AI News Trigger** (the name on old `main`) or **Daily AI News Email** after the new name is published on the default branch.
2. Select **Run workflow** and choose `ollama-with-AI-News-Agent`. The workflow file already exists on `main`, allowing manual dispatch to a branch containing the updated file. If the UI does not offer the workflow/branch, check publication and Actions permissions first.
3. Watch the run. It installs Python dependencies, validates credentials, installs Ollama, starts a loopback-only server, downloads the selected model and runs the pipeline once.
4. Successful steps must include model readiness and `Daily news email sent successfully`.
5. Confirm the digest arrives in `EMAIL_RECIPIENT`, including spam/junk checks.

This is a real email test. No delivery retry is configured: a timeout after SMTP acceptance could otherwise cause duplicate email. Inspect the inbox and run logs before repeating a failed job.

The runner has a 60-minute job limit; installation/model pull each have a 15-minute bound, and individual inference requests have a 180-second timeout. These limits report failures rather than claiming success. The first cloud run remains required to verify download speed, inference duration, SMTP authentication and actual inbox delivery.

The workflow follows [Ollama's Linux installation instructions](https://docs.ollama.com/linux) and uses the published [qwen3:1.7b model](https://ollama.com/library/qwen3:1.7b). Its server/model files exist only for that job; it downloads the model again for subsequent jobs.

## Step 5 ? enable the daily schedule from main

After the feature-branch test succeeds:

1. Review a pull request from `ollama-with-AI-News-Agent` into `main` and merge the tested changes.
2. Verify `.github/workflows/daily-news.yml` on `main` contains `45 16 * * *`.
3. Ensure `DAILY_NEWS_SCHEDULER` is not set to `disabled`.
4. Remove/disable both old scheduled keep-alive workflows. The prepared commit deletes redundant files and changes the remaining health workflow to manual only.
5. Monitor the first scheduled run and inbox delivery. GitHub runs schedules from the default branch; pushing the feature branch alone does not activate its schedule.
6. If Actions later reports the schedule disabled due to inactivity, re-enable it in the repository's Actions UI and check subsequent execution.

There is no paid Render Cron Job in this setup. Avoid another local scheduled copy if you do not want duplicate emails when the PC happens to be on.

## Step 6 ? redeploy the existing Render service on Free

Email delivery is independent of this step. You can keep the existing free web service and redeploy it as a status service:

1. Sign into [Render Dashboard](https://dashboard.render.com/), open the existing service and verify its instance type is **Free**.
2. In **Settings**, select repository `Talha-hub-wq/daily-ai-news` and branch `ollama-with-AI-News-Agent` (or `main` after the reviewed merge).
3. Use runtime **Python**, root directory empty, build command `pip install -r requirements.txt`.
4. Set start command to:

```bash
gunicorn app.main:app --workers 1 --bind 0.0.0.0:$PORT
```

5. Set health-check path `/`.
6. Set `SCHEDULE_TIME=22:00`, `SCHEDULE_TIMEZONE=Asia/Karachi`, and explicitly set `TRIGGER_TOKEN` to an empty value. The trigger/log endpoints remain disabled without a token. The GitHub job does not use those endpoints.
7. Existing NewsAPI/email credentials are unnecessary for this status-only service. Keep the actual sending credentials in GitHub Actions secrets. Gunicorn imports Flask without starting its internal scheduler.
8. Choose **Manual Deploy ? Deploy latest commit** and inspect build/start logs.
9. Open the service URL after startup. It should return HTTP 200 with the updated Ollama/timezone fields. The health response is still liveness only; it does not certify that a GitHub run or email succeeded.
10. Allow the free web service to sleep normally. No keep-alive cron is needed.

To create a new free status service instead, choose **New ? Web Service** with the same settings and **Free** instance. The updated [render.yaml](render.yaml) defines that web service as `daily-ai-news-status` with `plan: free`; it no longer creates a paid Cron Job. Applying a new Blueprint can create a separate service, so redeploy the existing service manually if you want to retain its URL. Check dashboard resource type/plan before applying.

Account access through the suggested Render integration is still needed for the assistant to perform dashboard changes directly. No dashboard redeployment has happened yet.

## Step 7 ? verify and monitor

- GitHub run finishes successfully and the inbox receives the digest.
- The scheduled workflow exists on `main`, at `45 16 * * *` for preparation, with the 22:00 delivery gate in code.
- The next day, confirm a scheduled run and actual inbox delivery; the expected time includes startup and processing delays.
- Render's status URL can sleep without affecting the GitHub email job.
- If the job fails, inspect Actions logs for model download, readiness, news fetch, inference timeout or SMTP authentication errors. A healthy Render URL does not resolve those failures.
- Do not enable both this full-pipeline workflow and a separate HTTP-trigger scheduler.

Local checks cover provider/configuration behavior, Pakistan timezone conversion, scheduled delivery windows, stale-run rejection and dated email headers; local Ollama/model readiness passes. Local tests do not replace the GitHub cloud run and inbox check. The repository is now unarchived and the branch published. Account connections/secrets, the cloud email test and schedule activation still need setup.

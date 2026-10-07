# Render redeployment: daily news at 10 PM Pakistan time

Reviewed October 7, 2026. Target branch: `ollama-with-AI-News-Agent`.

## What the existing deployment currently does

- [Existing Render web service](https://daily-ai-news-merl.onrender.com/) returned HTTP 200 after a cold-start timeout. Its response still advertised `13:25 (server local time)` and did not contain the new Ollama fields. This confirms that the old web app can start, not that it can fetch, summarize, or deliver email.
- The remote log endpoint contained startup entries only during this inspection. Previous email delivery cannot be established from those entries.
- The public GitHub repository's last push was May 7, 2026. Only `main` was published when checked; the Ollama feature branch was still local.
- The published daily workflow used `25 13 * * *`: 6:25 PM Pakistan time, not 10 PM. Its latest five available runs, June 12–16, failed. [Latest daily run](https://github.com/Talha-hub-wq/daily-ai-news/actions/runs/27638226768).
- Latest available keep-alive runs were June 17. Success there only establishes an HTTP request succeeded. It does not establish that email was sent. GitHub reported the workflows as active, but no recent scheduled execution was visible. The cause of the failures or missing runs was not established.

## Recommended deployment

Use a Render **Cron Job**, which starts the Python pipeline once a day, then exits. There is no web server to keep awake. Its schedule is:

```text
0 17 * * *
```

Render cron expressions use UTC; 17:00 UTC is **22:00 Asia/Karachi**. This is the job's start time. Fetching, local inference and mail delivery take additional time, so the email arrives after the job starts. [Render cron documentation](https://render.com/docs/cronjobs).

Render Cron Jobs are paid: the documented minimum is $1 per service per month, with active compute charges. Confirm the dashboard's current estimate before creating the service. An external Ollama server has its own hosting cost. [Render cron billing](https://render.com/docs/cronjobs).

The existing free web service sleeps after inactivity and blocks outbound SMTP ports 25, 465 and 587. The current sender uses SMTP 587, so keeping that free web service awake does not fix email delivery. [Render free-service limits](https://render.com/docs/free).

## Step 1 — choose where Ollama will run

The application uses Ollama's native `/api/tags` and `/api/chat` endpoints. It does not install Ollama or download model weights during the Render build.

`LLM_BASE_URL=http://127.0.0.1:11434` works on your PC. On Render it points to the Render container, which has no Ollama server. Choose one of these arrangements before deploying:

1. An existing always-on Ollama server reachable by Render through a secured HTTPS endpoint.
2. Your PC running Ollama, kept online with a secured tunnel or gateway reachable by Render. Delivery depends on that PC and its network remaining available.
3. A separate paid server with sufficient memory/compute for your model, running Ollama behind a secured HTTPS gateway.

The small Render Cron instance runs the Python news agent only; it is not sized to host `qwen3:8b`. Pull the selected model on the Ollama host and verify it appears in `ollama list`. Set `LLM_BASE_URL` to the gateway base URL, without `/api/chat`. If the gateway requires a bearer token, set `LLM_API_TOKEN`; the client sends it to both endpoints. Native Ollama itself does not enforce that gateway token.

## Step 2 — publish the prepared feature branch

Render can only deploy code available in GitHub. Current local edits have not been automatically committed or pushed by this guide.

```powershell
Set-Location 'D:\daily AI news'
git branch --show-current
git status --short
```

The branch should be `ollama-with-AI-News-Agent`. Review changes, then stage the application, configuration, tests and deployment documentation you want to publish. Never add `.env`, logs, virtual environments or credential files. Check the staged diff before committing:

```powershell
git diff --cached
git commit -m "Configure Ollama news agent for daily Render cron"
git push -u origin ollama-with-AI-News-Agent
```

This publishes the feature branch without replacing `main`. Render must explicitly select this branch. GitHub scheduled workflows run from the default branch, so feature-branch workflow edits alone do not replace the old schedules on `main`. [GitHub schedule rules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

## Step 3 — connect Render and GitHub

1. Sign into [Render Dashboard](https://dashboard.render.com/).
2. Connect the GitHub account that can access `Talha-hub-wq/daily-ai-news`.
3. Grant repository access if Render cannot list it.
4. If using the assistant to perform the deployment, connect the suggested Render integration and provide the Ollama endpoint configuration privately through Render's environment settings. Confirm the paid Cron approach before creating a billable service.

Dashboard inspection, deployment and billing changes require account access. Public health checks alone do not provide it.

## Step 4 — create a NEW Cron Job

Keep the existing web service while validating the replacement. Render does not allow changing an existing service's type to a Cron Job. The prepared Blueprint uses a distinct name, `daily-ai-news-digest`. [Render Blueprint specification](https://render.com/docs/blueprint-spec).

**Manual dashboard route:** select **New → Cron Job**, connect the repository, and enter:

| Setting | Value |
|---|---|
| Repository | `Talha-hub-wq/daily-ai-news` |
| Branch | `ollama-with-AI-News-Agent` |
| Name | `daily-ai-news-digest` |
| Runtime | Python |
| Root directory | Empty: project is at repository root |
| Build command | `pip install -r requirements.txt` |
| Command | `python app/main.py --run-once` |
| Schedule | `0 17 * * *` |
| Instance | Small paid instance for the Python agent; verify displayed price |

**Blueprint route:** select **New → Blueprint**, choose the same repository and branch, and use [render.yaml](render.yaml). Fill in the secret prompts and review the paid resource before applying. This file has been locally inspected; it has not yet been submitted to Render's account-level validator.

Do not use the Flask start command or Procfile for the Cron Job. The one-shot command performs one digest and exits nonzero on failure, allowing Render to report a failed run.

## Step 5 — enter environment variables

Reuse working credentials from your private environment or the existing Render service. Do not copy secrets into GitHub source, this document, or chat.

| Variable | Value / purpose |
|---|---|
| `LLM_PROVIDER` | `ollama` |
| `LLM_BASE_URL` | Your reachable, secured Ollama gateway URL |
| `LLM_MODEL` | `qwen3:8b`, or the model actually installed on that server |
| `LLM_API_TOKEN` | Optional bearer token required by your gateway; add manually if needed |
| `LLM_TIMEOUT` | `120`; increase only if needed for that server |
| `LLM_MAX_TOKENS` | `160` |
| `LLM_TEMPERATURE` | `0.3` |
| `NEWSAPI_KEY` | Your NewsAPI credential |
| `EMAIL_SENDER` | SMTP login/from address |
| `EMAIL_PASSWORD` | SMTP credential; Gmail generally uses an app password |
| `EMAIL_RECIPIENT` | Address that receives the digest |
| `SMTP_SERVER` | `smtp.gmail.com`, or your actual provider |
| `SMTP_PORT` | `587` for the current STARTTLS sender |
| `SCHEDULE_TIME` | `22:00` |
| `SCHEDULE_TIMEZONE` | `Asia/Karachi` |

There is no OpenAI key requirement. For this Cron Job, Render's cron expression controls execution; `SCHEDULE_TIME` affects only the internal scheduler and descriptive health response.

`TRIGGER_TOKEN` is unnecessary for a Cron Job because no HTTP endpoint is served. It is required if you choose the web-service/GitHub alternative below.

## Step 6 — build, then run once

1. Create the service only after reviewing the cost and endpoint configuration.
2. Watch the build logs. Dependency installation must complete successfully.
3. Use the Cron Job's **Trigger Run** action for one intentional test email.
4. Inspect run logs. The pipeline checks Ollama/model availability before fetching news. A failed connection/model check must cause a failed run rather than silently claiming deployment success.
5. Confirm logs contain `Daily news email sent successfully` and the job finishes successfully.
6. Confirm the message actually arrives at `EMAIL_RECIPIENT`; check spam if necessary. SMTP acceptance alone does not guarantee inbox placement.
7. Check the next scheduled run is 17:00 UTC / 10 PM Pakistan time. Keep monitoring the first daily run.

Local verification without fetching news or sending mail:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
.\venv\Scripts\python.exe app/main.py --check-services
```

The readiness command tests your locally configured Ollama connection. It does not establish that Render can reach that server, authenticate to SMTP, or fetch news. A manual Render run and inbox check are the end-to-end deployment verification.

## Step 7 — remove duplicate scheduling after a successful test

1. In GitHub → Actions, disable the old **Daily AI News Trigger** workflow if Render Cron is the selected scheduler.
2. Disable both old scheduled **Keep Alive** workflows. The repository previously had duplicate keep-alive files.
3. Stop any copy of the local continuously scheduled Python app if you no longer want it sending another daily digest.
4. After confirming the new service and email, suspend or remove the old Render web service if no longer needed.

The updated feature-branch daily workflow defaults to skipping scheduled delivery unless the repository variable `DAILY_NEWS_SCHEDULER=github` is set. The remaining health workflow is manual only. These changes take effect for scheduled GitHub execution only after they reach the default branch. You can disable the old workflows through GitHub immediately without merging the feature branch.

## Alternative: keep the web service and use GitHub scheduling

This is a separate deployment choice. Use one scheduler, not both.

1. Use a web instance that supports your SMTP delivery and configure its remote Ollama endpoint.
2. Deploy the feature branch with build command `pip install -r requirements.txt` and start command `gunicorn app.main:app --workers 1 --timeout 900`. Gunicorn imports the Flask app without starting its internal scheduler.
3. Set a long random `TRIGGER_TOKEN` privately on Render.
4. In GitHub → Settings → Secrets and variables → Actions, set secret `TRIGGER_TOKEN` to the same value, variable `RENDER_SERVICE_URL` to the HTTPS web-service URL, and variable `DAILY_NEWS_SCHEDULER` to `github`.
5. Review and merge the updated workflow into `main` when ready. Its schedule is `0 17 * * *`. GitHub can delay scheduled runs; it does not guarantee an exact 10 PM start. Public-repository schedules can be disabled after 60 days of inactivity. [GitHub schedule rules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
6. Run the workflow manually once and check the inbox. It warms the health endpoint with retries, then makes a single authenticated delivery request. The email request is deliberately not retried after a timeout because a retry could send a duplicate digest. Before manually retrying a failed request, inspect service logs and the inbox.

The new `/trigger-news` and `/logs` routes require `Authorization: Bearer <TRIGGER_TOKEN>`. A root health response remains public and reports liveness only. Do not mix the new protected app with the old unauthenticated workflow.

## Troubleshooting

| Symptom | Check |
|---|---|
| Ollama connection/model failure | Remote URL, gateway authentication, server uptime and `ollama list` on that host |
| SMTP timeout on free web service | Free Render's SMTP restrictions; move to the selected paid Cron setup |
| SMTP authentication failure | Provider login/app password, sender and STARTTLS settings |
| No news, job fails | NewsAPI key, rate limits and returned article availability |
| Inference timeout | Host resources and `LLM_TIMEOUT`; individual articles can fall back to source text after inference failure |
| Multiple emails | Old GitHub workflow, Render Cron and local app running simultaneously |
| No GitHub schedule activity | Default branch workflow, Actions settings and inactivity disabling |
| HTTP 401 | Missing/mismatched `TRIGGER_TOKEN` on the app and calling workflow |
| Healthy web page but no email | Liveness is not readiness; inspect the actual job and confirm inbox delivery |

## Work completed and remaining

Prepared locally: 17:00 UTC cron, explicit Pakistan timezone, corrected one-shot failure exit status, Ollama preflight and optional gateway bearer authentication, protected web endpoints, SMTP timeout, safer GitHub trigger workflow, and this deployment guide. Offline tests cover schedule conversion, authentication, readiness and failure behavior.

Still required: choose the reachable Ollama host, approve the paid deployment approach, connect Render account access, publish the feature branch, create/configure the service, run a real digest, verify the inbox and retire the old schedulers. No new Render service has been created by these local edits.

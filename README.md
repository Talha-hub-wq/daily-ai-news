# Daily AI & World News - Local Ollama Agent

A Python news pipeline that collects AI/world articles and supplementary tech/social stories, summarizes them on your computer using Ollama, and sends an HTML email digest.

**Active branch:** `ollama-with-AI-News-Agent`. The summarizer uses the native Ollama API. No OpenAI SDK, account, or API key is required.

## Features

- Up to five AI and five world articles from NewsAPI, with title deduplication.
- Hacker News and Nitter sections in the digest.
- Local summaries using your installed `qwen3:8b` model by default.
- Configurable provider URL, model, timeout, output token budget, and temperature.
- Source-text fallback if inference fails; no cloud-model fallback.
- SMTP delivery, daily scheduling, one-shot mode, and Flask trigger/log endpoints.
- Optional Twitter collection: unavailable `snscrape` returns an empty list instead of blocking startup. That separate Twitter list is not currently rendered in the email.

## Setup on Windows

1. Install/start [Ollama](https://ollama.com/download). This workspace already has Ollama and `qwen3:8b`; another machine must install/pull its selected model.
2. Check the installed models:

```powershell
ollama list
# Only needed if this model is not installed:
ollama pull qwen3:8b
```

3. Install the Python dependencies in a project environment:

```powershell
Set-Location 'D:\daily AI news'
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Gunicorn is for Linux hosting. The local Windows app starts with Python/Flask.

4. Create `.env` from [.env.example](.env.example) only if you do not already have a configured `.env`. Set NewsAPI and SMTP credentials privately. The migration preserves existing news/email values.

```dotenv
LLM_PROVIDER=ollama
LLM_BASE_URL=http://127.0.0.1:11434
LLM_MODEL=qwen3:8b
LLM_TIMEOUT=120
LLM_MAX_TOKENS=160
LLM_TEMPERATURE=0.3

NEWSAPI_KEY=your_newsapi_key
EMAIL_SENDER=sender@example.com
EMAIL_PASSWORD=your_smtp_password
EMAIL_RECIPIENT=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SCHEDULE_TIME=22:00
SCHEDULE_TIMEZONE=Asia/Karachi
```

Choose a model listed by `ollama list`. Keep the URL pointed at your Ollama server; it is a server base URL, without `/api/chat`. Restart the Python process after configuration changes. Values exported in the process environment take precedence over `.env`.

5. Validate configuration without sending an email:

```powershell
.\venv\Scripts\python.exe -c "from config.settings import validate_config; validate_config(); print('Configuration valid')"
```

## Run

Continuous Flask service plus internal scheduler:

```powershell
.\venv\Scripts\python.exe app/main.py
```

One intentional news fetch and email delivery:

```powershell
.\venv\Scripts\python.exe app/main.py --run-once
```

One-shot mode sends real email and exits nonzero on failure. The default internal schedule is `22:00` in `Asia/Karachi` (10 PM Pakistan time), independent of the host timezone. Use `python app/main.py --check-services` to check Ollama/model availability without fetching news or sending mail.

## Verify local inference without sending email

```powershell
.\venv\Scripts\python.exe -c "from app.llm_provider import create_llm_provider; print(create_llm_provider().summarize('Example', 'A team released a language model that summarizes documents locally on personal computers.'))"
```

This calls only the configured LLM server. It does not fetch news or send an email. Native Ollama uses POST `/api/chat` with `stream=false`, reads `message.content`, and supports generation options. [Ollama chat API](https://docs.ollama.com/api/chat).

Offline checks:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | Only supported inference provider |
| `LLM_BASE_URL` | `http://127.0.0.1:11434` | Ollama server base URL |
| `LLM_MODEL` | `qwen3:8b` | Installed model name |
| `LLM_TIMEOUT` | `120` | Positive HTTP timeout in seconds |
| `LLM_MAX_TOKENS` | `160` | Positive output-token budget (`num_predict`) |
| `LLM_TEMPERATURE` | `0.3` | Generation temperature, validated from 0 to 2 |
| `NEWSAPI_KEY` | Empty | Required news API credential |
| `EMAIL_SENDER` | Empty | Required SMTP login/from address |
| `EMAIL_PASSWORD` | Empty | Required SMTP password |
| `EMAIL_RECIPIENT` | Empty | Required recipient |
| `SMTP_SERVER` / `SMTP_PORT` | `smtp.gmail.com` / `587` | SMTP with STARTTLS |
| `SCHEDULE_TIME` | `22:00` | Internal daily job time |
| `SCHEDULE_TIMEZONE` | `Asia/Karachi` | Internal job timezone |
| `LLM_API_TOKEN` | Empty | Optional bearer token for a secured Ollama gateway |
| `TRIGGER_TOKEN` | Empty | Bearer token for HTTP trigger/log routes; blank disables access |
| `PORT` | `5000` | Direct Flask server port |

Actual story/post content takes priority over description metadata in summaries. Short text uses its title. Request/response failures use up to 150 characters of source text and log the exception type.

## HTTP routes and scheduling

| Method | Route | Behavior |
|---|---|---|
| GET | `/` | Static liveness response; does not test LLM/email readiness |
| POST | `/trigger-news` | Synchronous real delivery; 200/500 success/failure |
| GET | `/logs` | Last 50 lines of the local log file |

Trigger and log routes require `Authorization: Bearer <TRIGGER_TOKEN>`. A blank token disables access. The root response reports liveness only. The pipeline checks Ollama/model availability before fetching news; individual inference failures can still use source-text fallbacks.

The GitHub email workflow uses `0 17 * * *` (10 PM Pakistan time) and runs the full pipeline, including Ollama, on a standard cloud runner. It runs from the default branch; setting repository variable `DAILY_NEWS_SCHEDULER=disabled` pauses scheduled sends. GitHub may delay scheduled starts. The keep-alive workflow is manual only. Use one scheduler to avoid duplicate sends.

## Deployment

The selected deployment stays free and works while your PC is off. GitHub Actions installs Ollama, pulls `qwen3:1.7b`, fetches and summarizes news, and sends SMTP email. Render hosts the web/status service on its free plan and can sleep without affecting the email job. Your local model remains `qwen3:8b`.

Follow [the full deployment guide](RENDER_REDEPLOYMENT_GUIDE.md) to unarchive the GitHub repository, publish the feature branch, add Actions secrets, test delivery, merge the scheduled workflow into the default branch, and redeploy the existing free Render service.

Standard GitHub-hosted runners are free for public repositories; private repositories have separate allowances. [GitHub Actions billing](https://docs.github.com/en/actions/concepts/billing-and-usage). The first real workflow run is still required to verify CPU inference performance and inbox delivery.

[render.yaml](render.yaml) now describes a free web/status service, with HTTP delivery/log access disabled by a blank `TRIGGER_TOKEN`. It does not run Ollama or send email. Free Render web services block the SMTP ports used by this sender. [Render free-service limitations](https://render.com/docs/free).

The Procfile imports Flask through Gunicorn without starting the internal scheduler. A public health response establishes liveness only. The new GitHub workflow does not call that response or any Render trigger endpoint.

## Project layout

```text
app/
  main.py                 # Pipeline, CLI, Flask routes
  llm_provider.py         # Native Ollama client and configured factory
  summarizer.py           # Article summaries and fallback text
  news_fetcher.py          # NewsAPI AI/world articles
  hackernews_scraper.py    # Tech story source
  nitter_scraper.py        # Social posts
  twitter_scraper.py       # Optional scraper
  email_sender.py          # HTML and SMTP delivery
  scheduler.py             # In-memory scheduling
config/settings.py         # Environment loading and validation
.env.example               # Safe configuration template
templates/email_template.html
tests/test_local_llm.py     # Offline provider/config/pipeline tests
requirements.txt
render.yaml, Procfile, build.sh, runtime.txt
```

## Troubleshooting

- **Connection refused:** start Ollama and check `LLM_BASE_URL`.
- **Model not found:** run `ollama list`, then pull the desired model or correct `LLM_MODEL`.
- **Inference timeout:** allow more time in `LLM_TIMEOUT` or choose a model suitable for your hardware.
- **Fallback text instead of summaries:** review the local-LLM warning in `logs/app.log`; no cloud request is made.
- **No digest:** the current pipeline requires at least one AI or world article, even if supplementary sources have results.
- **Email failure:** inspect NewsAPI/SMTP settings and host network access. One-shot mode currently ignores the job Boolean, so exit code zero alone does not prove delivery.
- **Wrong Python dependencies:** this checkout has both `.venv` and `venv`; use the intended interpreter explicitly.
- **Google test import failure:** `test_google.py` references a disabled experimental function. Use `tests/` for current checks.

## Documentation

[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) contains the full architecture, inventory, routes, scheduling, source schemas, findings, and index of all older guides. Its local-provider sections have been updated for this branch.

Earlier Render/free-tier guides are retained as historical references and carry a migration notice. Their OpenAI instructions and cost/readiness assertions do not describe the active local branch.

Future work includes durable delivery history/idempotency, endpoint protection, bounded scraping, HTML escaping, preferences, multiple recipients, and a dashboard. These features are not implemented. The previous README asserted MIT licensing, but no standalone license file is present.

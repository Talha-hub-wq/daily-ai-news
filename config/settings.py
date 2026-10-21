"""Environment-backed configuration for the local Ollama news agent."""

import math
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
import pytz

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Local inference configuration; no API key or cloud-provider fallback.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:11434").strip().rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:8b").strip()
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "120"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "160"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_API_TOKEN = os.getenv("LLM_API_TOKEN", "")
TRIGGER_TOKEN = os.getenv("TRIGGER_TOKEN", "")

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "12:15")
SCHEDULE_TIMEZONE = os.getenv("SCHEDULE_TIMEZONE", "Asia/Karachi")

NEWS_LIMIT = 5
MAX_RETRIES = 3
RETRY_DELAY = 5


def validate_llm_config():
    """Validate inference settings without requiring email credentials."""
    if LLM_PROVIDER != "ollama":
        raise ValueError("LLM_PROVIDER must be 'ollama'; only local Ollama inference is supported")
    parsed = urlsplit(LLM_BASE_URL)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("LLM_BASE_URL must be an HTTP(S) server URL without credentials, query, or fragment")
    if not LLM_MODEL:
        raise ValueError("LLM_MODEL must name an installed Ollama model")
    if not math.isfinite(LLM_TIMEOUT) or LLM_TIMEOUT <= 0:
        raise ValueError("LLM_TIMEOUT must be a positive number of seconds")
    if LLM_MAX_TOKENS <= 0:
        raise ValueError("LLM_MAX_TOKENS must be a positive integer")
    if not math.isfinite(LLM_TEMPERATURE) or not 0 <= LLM_TEMPERATURE <= 2:
        raise ValueError("LLM_TEMPERATURE must be between 0 and 2")
    return True


def validate_config():
    """Validate news/email credentials and local LLM settings."""
    validate_llm_config()
    if not re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", SCHEDULE_TIME):
        raise ValueError("SCHEDULE_TIME must be HH:MM in 24-hour format")
    if SCHEDULE_TIMEZONE not in pytz.all_timezones_set:
        raise ValueError("SCHEDULE_TIMEZONE must be a valid IANA timezone")
    required = {
        "NEWSAPI_KEY": NEWSAPI_KEY,
        "EMAIL_SENDER": EMAIL_SENDER,
        "EMAIL_PASSWORD": EMAIL_PASSWORD,
        "EMAIL_RECIPIENT": EMAIL_RECIPIENT,
    }
    missing = [key for key, value in required.items() if not value.strip()]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return True

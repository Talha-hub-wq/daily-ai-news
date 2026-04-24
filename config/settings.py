import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Scheduling
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "22:00")  # 10:00 PM in 24-hour format

# API Settings
NEWS_LIMIT = 5
SUMMARIZER_MODEL = "gpt-3.5-turbo"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Validation
def validate_config():
    """Validate that all required configuration is present."""
    required = {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "EMAIL_SENDER": EMAIL_SENDER,
        "EMAIL_PASSWORD": EMAIL_PASSWORD,
        "EMAIL_RECIPIENT": EMAIL_RECIPIENT,
    }
    
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return True

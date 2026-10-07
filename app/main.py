import logging
import sys
import os
from pathlib import Path
from flask import Flask, jsonify
import threading
import hmac
from flask import request

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Create logs directory
os.makedirs('logs', exist_ok=True)

from config.settings import (
    # GOOGLE_API_KEY,
    # GOOGLE_CSE_ID,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT,
    SMTP_SERVER,
    SMTP_PORT,
    SCHEDULE_TIME,
    SCHEDULE_TIMEZONE,
    TRIGGER_TOKEN,
    LLM_PROVIDER,
    LLM_MODEL,
    NEWSAPI_KEY,
    validate_config
)
# from app.google_search import google_search
from app.news_fetcher import NewsFetcher
from app.summarizer import NewsSummarizer
from app.email_sender import EmailSender
from app.scheduler import NewsScheduler
from app.hackernews_scraper import get_hackernews_tech_stories
from app.nitter_scraper import get_nitter_tweets
from app.twitter_scraper import get_top_twitter_news

# -------------------- LOGGING --------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# -------------------- FLASK APP --------------------

app = Flask(__name__)

# -------------------- MAIN JOB --------------------

def send_daily_news():
    """Fetch, summarize and send news email."""
    try:
        logger.info("=" * 50)
        logger.info("Starting daily news update process...")
        logger.info("=" * 50)
        logger.info ('real time data and ai news')
        summarizer = NewsSummarizer()
        summarizer.check_ready()
        # Step 1: Fetch news
        fetcher = NewsFetcher(api_key=NEWSAPI_KEY)
        ai_news = fetcher.fetch_ai_news()
        world_news = fetcher.fetch_world_news()

        # # Step 1a: Fetch Google Search news
        # logger.info("Fetching Google Search news...")
        # ai_news = google_search("AI tools OR AI news", 5)
        # logger.info(f"Fetched {len(ai_news)} Google Search news")

        # # Step 1a: Fetch Google Search news
        # logger.info("Fetching Google world news...")
        # world_news  = google_search("latest world news 2026", 5)
        # logger.info(f"Fetched {len(world_news)} Google Search news") 

        # # Step 1a: Fetch Google Search news
        # logger.info("Fetching twitter  news...")
        # twitter_news  = google_search("site:twitter.com AI OR ChatGPT", 5)
        # logger.info(f"Fetched {len(twitter_news)} Google Search news")


        # Step 1b: Fetch HackerNews tech stories
        logger.info("Fetching HackerNews tech stories...")
        hackernews = get_hackernews_tech_stories(5)
        logger.info(f"Fetched {len(hackernews)} HackerNews stories")
        
        # Step 1c: Fetch Nitter tweets
        logger.info("Fetching Nitter tweets...")
        nitter_tweets = get_nitter_tweets("AI tools OR machine learning", 5)
        twitter_news = get_top_twitter_news("AI OR ChatGPT OR OpenAI lang:en min_faves:50", 5)
        logger.info(f"Fetched {len(twitter_news)} Twitter news")

        logger.info(f"Fetched {len(ai_news)} AI news, {len(world_news)} world news, {len(hackernews)} HackerNews stories, {len(twitter_news)} Twitter news")

        if not ai_news and not world_news:
            logger.warning("No news found. Email not sent.")
            return False

        # Step 2: Summarize
        ai_news = summarizer.summarize_articles(ai_news)
        world_news = summarizer.summarize_articles(world_news)
        hackernews = summarizer.summarize_articles(hackernews)
        nitter_tweets = summarizer.summarize_articles(nitter_tweets)
        twitter_news = summarizer.summarize_articles(twitter_news)
        logger.info("Articles summarized")

        # Step 3: Send Email
        email_sender = EmailSender(
            sender=EMAIL_SENDER,
            password=EMAIL_PASSWORD,
            smtp_server=SMTP_SERVER,
            smtp_port=SMTP_PORT
        )

        template_path = Path(__file__).parent.parent / "templates" / "email_template.html"

        success = email_sender.send_news_email(
            recipient=EMAIL_RECIPIENT,
            ai_news=ai_news,
            world_news=world_news,
            hackernews=hackernews,
            nitter_tweets=nitter_tweets,
            # twitter_news=twitter_news,
            html_template=str(template_path)
        )

        if success:
            logger.info("Daily news email sent successfully")
        else:
            logger.error("Failed to send email")
            return False

        logger.info("Daily news update completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error in send_daily_news: {e}", exc_info=True)
        return False


# -------------------- SCHEDULER --------------------

def start_scheduler():
    """Run scheduler in background."""
    try:
        scheduler = NewsScheduler()
        scheduler.schedule_daily(SCHEDULE_TIME, send_daily_news, SCHEDULE_TIMEZONE)
        logger.info(f"Scheduler set for daily run at {SCHEDULE_TIME} ({SCHEDULE_TIMEZONE})")
        scheduler.start()
    except Exception as e:
        logger.error(f"Scheduler error: {e}", exc_info=True)


# -------------------- FLASK ROUTES --------------------

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Daily AI News Automation",
        "next_run": f"Daily at {SCHEDULE_TIME} ({SCHEDULE_TIMEZONE})",
        "llm_provider": LLM_PROVIDER,
        "llm_model": LLM_MODEL,
        "readiness_checked": False
    }), 200


@app.route('/trigger-news', methods=['POST'])
def trigger_news_endpoint():
    if not authorized_request():
        return jsonify({"status": "unauthorized"}), 401
    try:
        logger.info("Manual trigger via API")
        success = send_daily_news()

        if success:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 500

    except Exception as e:
        logger.error(f"Trigger error: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    if not authorized_request():
        return jsonify({"status": "unauthorized"}), 401
    try:
        log_file = 'logs/app.log'
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = f.readlines()[-50:]
            return jsonify({"logs": logs}), 200
        return jsonify({"error": "Log file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------- MAIN --------------------

def authorized_request():
    """Webhook/log access is disabled until a private trigger token is set."""
    expected = f"Bearer {TRIGGER_TOKEN}"
    return bool(TRIGGER_TOKEN) and hmac.compare_digest(
        request.headers.get("Authorization", "").encode("utf-8"), expected.encode("utf-8")
    )

def main():
    try:
        logger.info("Validating configuration...")
        validate_config()
        logger.info("Configuration validated")

        # CLI MODE
        if len(sys.argv) > 1:
            if sys.argv[1] == "--check-services":
                NewsSummarizer().check_ready()
                logger.info("Ollama readiness check passed; no news fetched or email sent")
                return
            if sys.argv[1] == "--run-once":
                logger.info("Running in test mode...")
                if not send_daily_news():
                    sys.exit(1)
                return

        # START SCHEDULER THREAD
        scheduler_thread = threading.Thread(target=start_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()

        logger.info("Scheduler thread started")

        # START FLASK
        port = int(os.getenv("PORT", 5000))
        logger.info(f"Starting Flask server on port {port}")
        app.run(host="0.0.0.0", port=port, debug=False)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

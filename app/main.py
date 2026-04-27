import logging
import sys
import os
from pathlib import Path
from flask import Flask, jsonify
import threading

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Create logs directory
os.makedirs('logs', exist_ok=True)

from config.settings import (
    OPENAI_API_KEY,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT,
    SMTP_SERVER,
    SMTP_PORT,
    SCHEDULE_TIME,
    NEWSAPI_KEY,
    validate_config
)

from app.news_fetcher import NewsFetcher
from app.summarizer import NewsSummarizer
from app.email_sender import EmailSender
from app.scheduler import NewsScheduler

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

        # Step 1: Fetch news
        fetcher = NewsFetcher(api_key=NEWSAPI_KEY)
        ai_news = fetcher.fetch_ai_news()
        world_news = fetcher.fetch_world_news()

        logger.info(f"Fetched {len(ai_news)} AI news and {len(world_news)} world news")

        if not ai_news and not world_news:
            logger.warning("No news found. Email not sent.")
            return False

        # Step 2: Summarize
        summarizer = NewsSummarizer(api_key=OPENAI_API_KEY)
        ai_news = summarizer.summarize_articles(ai_news)
        world_news = summarizer.summarize_articles(world_news)

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
        scheduler.schedule_daily(SCHEDULE_TIME, send_daily_news)
        logger.info(f"Scheduler set for daily run at {SCHEDULE_TIME}")
        scheduler.start()
    except Exception as e:
        logger.error(f"Scheduler error: {e}", exc_info=True)


# -------------------- FLASK ROUTES --------------------

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Daily AI News Automation",
        "next_run": f"Daily at {SCHEDULE_TIME} (server local time)"
    }), 200


@app.route('/trigger-news', methods=['POST'])
def trigger_news_endpoint():
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

def main():
    try:
        logger.info("Validating configuration...")
        validate_config()
        logger.info("Configuration validated")

        # CLI MODE
        if len(sys.argv) > 1:
            if sys.argv[1] == "--run-once":
                logger.info("Running in test mode...")
                send_daily_news()
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


# import logging
# import sys
# import os
# from pathlib import Path
# from flask import Flask, jsonify
# import threading
# import time

# # Add parent directory to path
# sys.path.insert(0, str(Path(__file__).parent.parent))

# # Create logs directory BEFORE setting up logging
# os.makedirs('logs', exist_ok=True)

# from config.settings import (
#     OPENAI_API_KEY,
#     EMAIL_SENDER,
#     EMAIL_PASSWORD,
#     EMAIL_RECIPIENT,
#     SMTP_SERVER,
#     SMTP_PORT,
#     SCHEDULE_TIME,
#     NEWSAPI_KEY,
#     validate_config
# )
# from app.news_fetcher import NewsFetcher
# from app.summarizer import NewsSummarizer
# from app.email_sender import EmailSender
# from app.scheduler import NewsScheduler

# # Setup logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('logs/app.log'),
#         logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger(__name__)

# # Initialize Flask app
# app = Flask(__name__)


# def send_daily_news():
#     """Main function to fetch news, summarize, and send email."""
#     try:
#         logger.info("=" * 50)
#         logger.info("Starting daily news update process...")
#         logger.info("=" * 50)
        
#         # Step 1: Fetch news
#         logger.info("Step 1: Fetching news...")
#         fetcher = NewsFetcher(api_key=NEWSAPI_KEY)
        
#         ai_news = fetcher.fetch_ai_news()
#         world_news = fetcher.fetch_world_news()
        
#         logger.info(f"Fetched {len(ai_news)} AI news and {len(world_news)} world news")
        
#         if not ai_news and not world_news:
#             logger.warning("No news found. Email not sent.")
#             return False
        
#         # Step 2: Summarize news
#         logger.info("Step 2: Summarizing articles...")
#         summarizer = NewsSummarizer(api_key=OPENAI_API_KEY)
        
#         ai_news = summarizer.summarize_articles(ai_news)
#         world_news = summarizer.summarize_articles(world_news)
        
#         logger.info("Articles summarized")
        
#         # Step 3: Send email
#         logger.info("Step 3: Sending email...")
#         email_sender = EmailSender(
#             sender=EMAIL_SENDER,
#             password=EMAIL_PASSWORD,
#             smtp_server=SMTP_SERVER,
#             smtp_port=SMTP_PORT
#         )
        
#         template_path = Path(__file__).parent.parent / "templates" / "email_template.html"
        
#         success = email_sender.send_news_email(
#             recipient=EMAIL_RECIPIENT,
#             ai_news=ai_news,
#             world_news=world_news,
#             html_template=str(template_path)
#         )
        
#         if success:
#             logger.info("✓ Daily news email sent successfully")
#         else:
#             logger.error("✗ Failed to send email")
#             return False
        
#         logger.info("=" * 50)
#         logger.info("Daily news update completed successfully")
#         logger.info("=" * 50)
        
#         return True
    
#     except Exception as e:
#         logger.error(f"Error in send_daily_news: {e}", exc_info=True)
#         return False


# def main():
#     """Main entry point."""
#     try:
#         # Validate configuration
#         logger.info("Validating configuration...")
#         validate_config()
#         logger.info("✓ Configuration validated")
        
#         # Check for command line arguments
#         if len(sys.argv) > 1:
#             if sys.argv[1] == "--run-once":
#                 logger.info("Running news update once (test mode)...")
#                 send_daily_news()
#                 return
#             elif sys.argv[1] == "--help":
#                 print("Usage: python main.py [OPTIONS]")
#                 print("Options:")
#                 print("  --run-once    Run the news update once (for testing)")
#                 print("  --help        Show this help message")
#                 print("\nWithout options, starts Flask web service (for Render)")
#                 return
        
#         # Start Flask web service (for Render deployment)
#         logger.info("Starting Flask web service on port 5000...")
#         logger.info("Available endpoints:")
#         logger.info("  GET  / → Health check")
#         logger.info("  POST /trigger-news → Trigger news update")
        
#         port = int(os.getenv("PORT", 5000))
#         app.run(host="0.0.0.0", port=port, debug=False)
    
#     except ValueError as e:
#         logger.error(f"Configuration error: {e}")
#         print(f"\n❌ Configuration Error: {e}")
#         print("\nPlease set up your environment variables. See README.md for instructions.")
#         sys.exit(1)
#     except KeyboardInterrupt:
#         logger.info("Application stopped by user")
#         print("\n👋 Application stopped")
#     except Exception as e:
#         logger.error(f"Fatal error: {e}", exc_info=True)
#         print(f"\n❌ Error: {e}")
#         sys.exit(1)


# # Flask Routes

# @app.route('/', methods=['GET'])
# def health_check():
#     """Health check endpoint - used by Render to verify service is running."""
#     return jsonify({
#         "status": "healthy",
#         "service": "Daily AI News Automation",
#         "version": "1.0",
#         "next_run": f"Daily at {SCHEDULE_TIME} UTC"
#     }), 200


# @app.route('/trigger-news', methods=['POST'])
# def trigger_news_endpoint():
#     """Endpoint to trigger news update via HTTP request."""
#     try:
#         logger.info("News update triggered via HTTP endpoint")
#         success = send_daily_news()
        
#         if success:
#             return jsonify({
#                 "status": "success",
#                 "message": "News email sent successfully"
#             }), 200
#         else:
#             return jsonify({
#                 "status": "error",
#                 "message": "Failed to send news email"
#             }), 500
    
#     except Exception as e:
#         logger.error(f"Error in trigger endpoint: {e}", exc_info=True)
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500


# @app.route('/logs', methods=['GET'])
# def get_logs():
#     """Endpoint to view recent logs."""
#     try:
#         log_file = 'logs/app.log'
#         if os.path.exists(log_file):
#             with open(log_file, 'r') as f:
#                 logs = f.readlines()
#             # Return last 50 lines
#             recent_logs = logs[-50:]
#             return jsonify({
#                 "status": "success",
#                 "logs": recent_logs
#             }), 200
#         else:
#             return jsonify({
#                 "status": "error",
#                 "message": "Log file not found"
#             }), 404
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500


# if __name__ == "__main__":
#     main()

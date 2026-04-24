import logging
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Create logs directory BEFORE setting up logging
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def send_daily_news():
    """Main function to fetch news, summarize, and send email."""
    try:
        logger.info("=" * 50)
        logger.info("Starting daily news update process...")
        logger.info("=" * 50)
        
        # Step 1: Fetch news
        logger.info("Step 1: Fetching news...")
        fetcher = NewsFetcher(api_key=NEWSAPI_KEY)
        
        ai_news = fetcher.fetch_ai_news()
        world_news = fetcher.fetch_world_news()
        
        logger.info(f"Fetched {len(ai_news)} AI news and {len(world_news)} world news")
        
        if not ai_news and not world_news:
            logger.warning("No news found. Email not sent.")
            return False
        
        # Step 2: Summarize news
        logger.info("Step 2: Summarizing articles...")
        summarizer = NewsSummarizer(api_key=OPENAI_API_KEY)
        
        ai_news = summarizer.summarize_articles(ai_news)
        world_news = summarizer.summarize_articles(world_news)
        
        logger.info("Articles summarized")
        
        # Step 3: Send email
        logger.info("Step 3: Sending email...")
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
            logger.info("✓ Daily news email sent successfully")
        else:
            logger.error("✗ Failed to send email")
            return False
        
        logger.info("=" * 50)
        logger.info("Daily news update completed successfully")
        logger.info("=" * 50)
        
        return True
    
    except Exception as e:
        logger.error(f"Error in send_daily_news: {e}", exc_info=True)
        return False


def main():
    """Main entry point."""
    try:
        # Validate configuration
        logger.info("Validating configuration...")
        validate_config()
        logger.info("✓ Configuration validated")
        
        # Check for command line arguments
        if len(sys.argv) > 1:
            if sys.argv[1] == "--run-once":
                logger.info("Running news update once (test mode)...")
                send_daily_news()
                return
            elif sys.argv[1] == "--help":
                print("Usage: python main.py [OPTIONS]")
                print("Options:")
                print("  --run-once    Run the news update once (for testing)")
                print("  --help        Show this help message")
                print("\nWithout options, the app will start the scheduler")
                return
        
        # Start scheduler
        logger.info(f"Starting scheduler. Daily email will be sent at {SCHEDULE_TIME}")
        scheduler = NewsScheduler()
        scheduler.schedule_daily(SCHEDULE_TIME, send_daily_news)
        scheduler.start()
    
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease set up your environment variables. See README.md for instructions.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        print("\n👋 Application stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

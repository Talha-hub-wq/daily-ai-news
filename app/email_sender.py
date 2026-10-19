import smtplib
import logging
from datetime import datetime, timezone
from email.utils import format_datetime, make_msgid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import pytz

from config.settings import SCHEDULE_TIMEZONE

logger = logging.getLogger(__name__)


class EmailSender:
    """Send formatted email with news updates."""
    
    def __init__(self, sender: str, password: str, smtp_server: str, smtp_port: int):
        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_news_email(
        self,
        recipient: str,
        ai_news: List[Dict],
        world_news: List[Dict],
        hackernews: List[Dict] = None,
        nitter_tweets: List[Dict] = None,
        html_template: str = None
    ) -> bool:
        """Send formatted news email."""
        try:
            generated_at = datetime.now(timezone.utc).astimezone(pytz.timezone(SCHEDULE_TIMEZONE))
            digest_date = generated_at.strftime("%Y-%m-%d")
            if hackernews is None:
                hackernews = []
            if nitter_tweets is None:
                nitter_tweets = []
                
            # Read template
            with open(html_template, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Build email content
            html_content = self._build_html_content(template, ai_news, world_news, hackernews, nitter_tweets)
            html_content = html_content.replace("{{ DIGEST_DATE }}", digest_date)
            html_content = html_content.replace(
                "{{ GENERATED_AT }}", generated_at.strftime("%Y-%m-%d %I:%M %p %Z")
            )
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Daily AI & World News - {digest_date}"
            message["Date"] = format_datetime(generated_at)
            message["Message-ID"] = make_msgid(idstring=f"daily-news.{digest_date}")
            message["X-Digest-Timezone"] = SCHEDULE_TIMEZONE
            message["X-Digest-Generated-At"] = generated_at.isoformat()
            message["From"] = self.sender
            message["To"] = recipient
            
            # Attach HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            self._send_smtp(recipient, message)
            
            logger.info("SMTP accepted digest for %s, generated at %s", digest_date, generated_at.isoformat())
            return True
        except FileNotFoundError:
            logger.error(f"Email template not found: {html_template}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _build_html_content(
        self,
        template: str,
        ai_news: List[Dict],
        world_news: List[Dict],
        hackernews: List[Dict] = None,
        nitter_tweets: List[Dict] = None
    ) -> str:
        """Build HTML email content from template and news data."""
        
        # Build AI news section
        ai_html = ""
        for i, article in enumerate(ai_news, 1):
            ai_html += f"""
            <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #e0e0e0;">
                <h4 style="margin: 0 0 10px 0; color: #1a73e8;">
                    {i}. {article.get('title', 'No Title')}
                </h4>
                <p style="margin: 8px 0; color: #555; font-size: 14px;">
                    {article.get('summary', article.get('description', 'No summary available'))}
                </p>
                <p style="margin: 8px 0; font-size: 12px;">
                    <strong>Source:</strong> {article.get('source', 'Unknown')}
                </p>
                <p style="margin: 0; font-size: 12px;">
                    <a href="{article.get('url', '#')}" style="color: #1a73e8; text-decoration: none;">
                        Read full article →
                    </a>
                </p>
            </div>
            """
        
        # Build world news section
        world_html = ""
        for i, article in enumerate(world_news, 1):
            world_html += f"""
            <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #e0e0e0;">
                <h4 style="margin: 0 0 10px 0; color: #1a73e8;">
                    {i}. {article.get('title', 'No Title')}
                </h4>
                <p style="margin: 8px 0; color: #555; font-size: 14px;">
                    {article.get('summary', article.get('description', 'No summary available'))}
                </p>
                <p style="margin: 8px 0; font-size: 12px;">
                    <strong>Source:</strong> {article.get('source', 'Unknown')}
                </p>
                <p style="margin: 0; font-size: 12px;">
                    <a href="{article.get('url', '#')}" style="color: #1a73e8; text-decoration: none;">
                        Read full article →
                    </a>
                </p>
            </div>
            """
        
        # Replace placeholders
        html_content = template.replace("{{ AI_NEWS }}", ai_html)
        html_content = html_content.replace("{{ WORLD_NEWS }}", world_html)
        
        # Build HackerNews section
        hackernews_html = ""
        if hackernews:
            for i, story in enumerate(hackernews, 1):
                hackernews_html += f"""
            <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #e0e0e0;">
                <h4 style="margin: 0 0 10px 0; color: #1a73e8;">
                    {i}. {story.get('title', 'No Title')}
                </h4>
                <p style="margin: 8px 0; color: #555; font-size: 14px;">
                    {story.get('summary', story.get('content', 'No content available'))}
                </p>
                <p style="margin: 8px 0; font-size: 12px;">
                    <strong>Author:</strong> {story.get('author', 'Unknown')} | <strong>Points:</strong> {story.get('points', 0)}
                </p>
                <p style="margin: 0; font-size: 12px;">
                    <a href="{story.get('url', '#')}" style="color: #1a73e8; text-decoration: none;">
                        Read on HackerNews →
                    </a>
                </p>
            </div>
            """
        
        html_content = html_content.replace("{{ HACKERNEWS }}", hackernews_html)
        
        # Build Nitter section
        nitter_html = ""
        if nitter_tweets:
            for i, tweet in enumerate(nitter_tweets, 1):
                nitter_html += f"""
            <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #e0e0e0;">
                <h4 style="margin: 0 0 10px 0; color: #1a73e8;">
                    {i}. {tweet.get('title', 'No Title')}
                </h4>
                <p style="margin: 8px 0; color: #555; font-size: 14px;">
                    {tweet.get('summary', tweet.get('content', 'No content available'))}
                </p>
                <p style="margin: 8px 0; font-size: 12px;">
                    <strong>Author:</strong> @{tweet.get('author', 'Unknown')}
                </p>
                <p style="margin: 0; font-size: 12px;">
                    <a href="{tweet.get('url', '#')}" style="color: #1a73e8; text-decoration: none;">
                        View Tweet →
                    </a>
                </p>
            </div>
            """
        
        html_content = html_content.replace("{{ NITTER }}", nitter_html)
        
        return html_content
    
    def _send_smtp(self, recipient: str, message: MIMEMultipart) -> None:
        """Send email via SMTP."""
        with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, recipient, message.as_string())


if __name__ == "__main__":
    print("Email Sender module loaded")

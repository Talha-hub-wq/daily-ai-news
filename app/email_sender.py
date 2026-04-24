import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

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
        html_template: str
    ) -> bool:
        """Send formatted news email."""
        try:
            # Read template
            with open(html_template, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Build email content
            html_content = self._build_html_content(template, ai_news, world_news)
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Daily AI & World News"
            message["From"] = self.sender
            message["To"] = recipient
            
            # Attach HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            self._send_smtp(recipient, message)
            
            logger.info(f"Email sent successfully to {recipient}")
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
        world_news: List[Dict]
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
        
        return html_content
    
    def _send_smtp(self, recipient: str, message: MIMEMultipart) -> None:
        """Send email via SMTP."""
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, recipient, message.as_string())


if __name__ == "__main__":
    print("Email Sender module loaded")

import openai
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class NewsSummarizer:
    """Summarize news articles using OpenAI API."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.max_tokens = 100
    
    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        """Summarize a list of articles."""
        summarized = []
        
        for article in articles:
            try:
                summary = self._summarize_single(
                    article.get("title", ""),
                    article.get("description", "")
                )
                
                article["summary"] = summary
                summarized.append(article)
            
            except Exception as e:
                logger.error(f"Error summarizing article '{article.get('title')}': {e}")
                # Use original description as fallback
                article["summary"] = article.get("description", "No summary available")
                summarized.append(article)
        
        return summarized
    
    def _summarize_single(self, title: str, description: str) -> str:
        """Summarize a single article."""
        if not description or len(description) < 20:
            return description if description else "No description available"
        
        prompt = f"""Summarize the following news item in 2-3 sentences, focusing on key facts:

Title: {title}
Description: {description}

Provide a concise summary:"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.5
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        
        except openai.error.RateLimitError:
            logger.warning("OpenAI rate limit hit, using original description")
            return description
        except openai.error.APIError as e:
            logger.warning(f"OpenAI API error: {e}, using original description")
            return description
        except Exception as e:
            logger.error(f"Unexpected error in summarization: {e}")
            return description


if __name__ == "__main__":
    print("News Summarizer module loaded")

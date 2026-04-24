import requests
import json
import logging
from typing import List, Dict
from datetime import datetime, timedelta
from urllib.parse import quote

logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetch AI and world news from multiple sources."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.newsapi_url = "https://newsapi.org/v2/everything"
        self.timeout = 10
    
    def fetch_ai_news(self) -> List[Dict]:
        """Fetch latest AI news."""
        try:
            queries = [
                "latest AI news 2026",
                "new AI tools released",
                "AI advancements breakthrough",
                "artificial intelligence products"
            ]
            
            all_articles = []
            
            for query in queries:
                articles = self._fetch_from_newsapi(query, "AI news")
                all_articles.extend(articles)
                if len(all_articles) >= 5:
                    break
            
            # Remove duplicates and return top 5
            unique_articles = self._deduplicate_articles(all_articles)
            return unique_articles[:5]
        
        except Exception as e:
            logger.error(f"Error fetching AI news: {e}")
            return []
    
    def fetch_world_news(self) -> List[Dict]:
        """Fetch latest world news."""
        try:
            articles = self._fetch_from_newsapi("top world news today", "world news")
            unique_articles = self._deduplicate_articles(articles)
            return unique_articles[:5]
        
        except Exception as e:
            logger.error(f"Error fetching world news: {e}")
            return []
    
    def _fetch_from_newsapi(self, query: str, category: str) -> List[Dict]:
        """Fetch articles from NewsAPI."""
        try:
            # Calculate date from last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            params = {
                "q": query,
                "sortBy": "publishedAt",
                "language": "en",
                "from": from_date,
                "apiKey": self.api_key,
                "pageSize": 10
            }
            
            response = requests.get(self.newsapi_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "ok":
                logger.warning(f"NewsAPI returned status: {data.get('status')}")
                return []
            
            articles = []
            for article in data.get("articles", []):
                if article.get("title") and article.get("url"):
                    articles.append({
                        "title": article["title"],
                        "description": article.get("description", ""),
                        "url": article["url"],
                        "source": article.get("source", {}).get("name", "Unknown"),
                        "image": article.get("urlToImage"),
                        "published_at": article.get("publishedAt"),
                        "category": category
                    })
            
            return articles
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from NewsAPI for '{query}': {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing NewsAPI response: {e}")
            return []
    
    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title."""
        seen_titles = set()
        unique = []
        
        for article in articles:
            title = article.get("title", "").lower().strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique.append(article)
        
        return unique


if __name__ == "__main__":
    # Test with dummy API key (will fail without real key)
    fetcher = NewsFetcher(api_key="test_key")
    print("News Fetcher initialized")

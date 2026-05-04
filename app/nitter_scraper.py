import logging
import requests
from typing import List, Dict
from html.parser import HTMLParser
import re

logger = logging.getLogger(__name__)


class TweetParser(HTMLParser):
    """Parse tweet HTML from Nitter."""
    
    def __init__(self):
        super().__init__()
        self.tweets = []
        self.current_tweet = {}
        self.in_tweet = False
        self.in_text = False
        self.current_text = ""


def get_nitter_tweets(query: str = "AI news", limit: int = 5) -> List[Dict]:
    """
    Fetch tweets from Nitter (alternative Twitter frontend).
    
    Args:
        query: Search query (default: "AI news")
        limit: Number of tweets to fetch (default: 5)
    
    Returns:
        List of tweet dictionaries with title, content, url, author
    """
    tweets = []
    
    try:
        logger.info(f"Fetching Nitter tweets with query: '{query}'")
        
        # List of Nitter instances to try (some might be down)
        nitter_instances = [
            "https://nitter.net",
            "https://nitter.1d4.us",
            "https://nitter.esmailelbob.xyz",
            "https://nitter.privacydev.net",
        ]
        
        search_url = None
        for instance in nitter_instances:
            try:
                # Try to search on this instance
                url = f"{instance}/search?q={query.replace(' ', '%20')}&f=live"
                response = requests.get(url, timeout=10, allow_redirects=False)
                
                if response.status_code == 200:
                    search_url = url
                    break
            except:
                continue
        
        if not search_url:
            logger.warning("No working Nitter instance found")
            return []
        
        # Fetch tweets
        response = requests.get(search_url, timeout=15)
        response.raise_for_status()
        html_content = response.text
        
        # Simple parsing of tweet data using regex
        tweet_pattern = r'<div class="tweet">.*?<a href="(.*?)">(.*?)</a>.*?<p>(.*?)</p>'
        matches = re.findall(tweet_pattern, html_content, re.DOTALL)
        
        for url, author_html, tweet_text in matches:
            if len(tweets) >= limit:
                break
            
            try:
                # Extract author
                author_match = re.search(r'>@(\w+)<', author_html)
                author = author_match.group(1) if author_match else "Unknown"
                
                # Clean tweet text
                tweet_text = re.sub(r'<[^>]+>', '', tweet_text).strip()
                
                if len(tweet_text) < 20:
                    continue
                
                tweet_data = {
                    "title": tweet_text[:80],
                    "content": tweet_text,
                    "url": f"https://twitter.com{url}" if url.startswith('/') else url,
                    "author": author,
                    "likes": 0  # Nitter might not expose likes
                }
                
                tweets.append(tweet_data)
                
            except Exception as e:
                logger.warning(f"Error parsing tweet: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(tweets)} Nitter tweets")
        return tweets
    
    except Exception as e:
        logger.error(f"Error fetching Nitter tweets: {e}")
        return []

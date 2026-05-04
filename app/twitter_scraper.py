import logging
import snscrape.modules.twitter as sntwitter
from typing import List, Dict

logger = logging.getLogger(__name__)


def get_top_twitter_news(query: str = "AI tools OR AI news", limit: int = 5) -> List[Dict]:
    """
    Fetch top tweets based on query using snscrape.
    
    Args:
        query: Search query (default: "AI tools OR AI news")
        limit: Number of tweets to fetch (default: 5)
    
    Returns:
        List of tweet dictionaries with title, content, url, author, likes
    """
    tweets = []
    
    try:
        logger.info(f"Fetching Twitter news with query: '{query}'")
        
        # Create scraper
        scraper = sntwitter.TwitterSearchScraper(query)
        
        # Collect tweets
        tweet_count = 0
        for tweet in scraper.get_items():
            if tweet_count >= limit * 3:  # Fetch more to filter
                break
            
            try:
                # Skip replies and retweets
                if tweet.inReplyToTweetId is not None or tweet.retweetedTweet is not None:
                    continue
                
                # Filter by likes (minimum 50)
                if tweet.likeCount < 50:
                    continue
                
                # Check if tweet language is English (if language info available)
                # Note: snscrape may not always provide language, so we'll be lenient
                
                # Extract tweet data
                tweet_text = tweet.content
                if len(tweet_text) == 0:
                    continue
                
                tweet_data = {
                    "title": tweet_text[:80],  # First 80 characters as title
                    "content": tweet_text,
                    "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}",
                    "author": tweet.user.username,
                    "likes": tweet.likeCount
                }
                
                tweets.append(tweet_data)
                tweet_count += 1
                
                if len(tweets) >= limit:
                    break
                    
            except Exception as e:
                logger.warning(f"Error processing tweet: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(tweets)} Twitter news articles")
        return tweets
    
    except Exception as e:
        logger.error(f"Error fetching Twitter news: {e}")
        return []

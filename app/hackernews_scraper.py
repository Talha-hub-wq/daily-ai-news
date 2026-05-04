import logging
import requests
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


def get_hackernews_tech_stories(limit: int = 5) -> List[Dict]:
    """
    Fetch top tech/AI stories from HackerNews.
    
    Args:
        limit: Number of stories to fetch (default: 5)
    
    Returns:
        List of story dictionaries with title, content, url, points
    """
    stories = []
    
    try:
        logger.info(f"Fetching HackerNews tech stories...")
        
        # Get top story IDs
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:30]  # Get top 30 to filter
        
        # Fetch stories and filter for tech/AI content
        for story_id in story_ids:
            if len(stories) >= limit:
                break
            
            try:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=5)
                story_response.raise_for_status()
                story = story_response.json()
                
                # Skip if deleted or dead
                if not story or story.get('deleted') or story.get('dead'):
                    continue
                
                # Only include stories (not comments, polls)
                if story.get('type') != 'story':
                    continue
                
                # Check if it's tech/AI related
                title = story.get('title', '').lower()
                keywords = ['ai', 'artificial intelligence', 'machine learning', 'neural', 
                           'llm', 'tech', 'python', 'algorithm', 'startup', 'gpu']
                
                if not any(keyword in title for keyword in keywords):
                    continue
                
                story_data = {
                    "title": story.get('title', 'No Title'),
                    "content": f"{story.get('title', 'No Title')} - {story.get('score', 0)} points",
                    "url": story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    "author": story.get('by', 'Anonymous'),
                    "points": story.get('score', 0),
                    "comments": story.get('descendants', 0)
                }
                
                stories.append(story_data)
                
            except requests.RequestException as e:
                logger.warning(f"Error fetching story {story_id}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Error processing story {story_id}: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(stories)} HackerNews tech stories")
        return stories
    
    except Exception as e:
        logger.error(f"Error fetching HackerNews stories: {e}")
        return []

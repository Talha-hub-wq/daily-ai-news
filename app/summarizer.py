"""Summarize news with local inference and a source-text fallback."""

import logging
from typing import Dict, List

from app.llm_provider import create_llm_provider

logger = logging.getLogger(__name__)


class NewsSummarizer:
    def __init__(self, provider=None):
        self.provider = provider if provider is not None else create_llm_provider()

    def check_ready(self):
        return self.provider.check_ready()

    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        summarized = []
        for article in articles:
            # Prefer actual story/post content over likes or points metadata.
            title = str(article.get("title") or "")
            text = str(article.get("content") or article.get("description") or title)
            if not text or len(text) < 20:
                article["summary"] = title or "No summary available"
            else:
                article["summary"] = self._summarize_single(title, text)
            summarized.append(article)
        return summarized

    def _summarize_single(self, title: str, text: str) -> str:
        try:
            return self.provider.summarize(title, text)
        except Exception as exc:
            # Avoid logging request bodies, raw URLs, or credentials.
            logger.warning("Local LLM summary failed (%s); using source text", type(exc).__name__)
            return text[:150]

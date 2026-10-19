"""Offline contract checks for local inference, failure handling, and config."""

import unittest
from unittest.mock import Mock, patch

import requests

from app.llm_provider import OllamaProvider, create_llm_provider
from app.summarizer import NewsSummarizer
from config import settings


class OllamaProviderTests(unittest.TestCase):
    @patch("app.llm_provider.requests.post")
    def test_native_chat_contract(self, post):
        post.return_value.json.return_value = {"message": {"content": "  Local summary.  "}}
        provider = OllamaProvider("http://localhost:11434/", "test-model", 45, 80, 0.2)
        self.assertEqual(provider.summarize("Title", "Source text"), "Local summary.")
        args, kwargs = post.call_args
        self.assertEqual(args, ("http://localhost:11434/api/chat",))
        self.assertEqual(kwargs["timeout"], 45)
        payload = kwargs["json"]
        self.assertEqual(payload["model"], "test-model")
        self.assertFalse(payload["stream"])
        self.assertFalse(payload["think"])
        self.assertEqual(payload["options"], {"num_predict": 80, "temperature": 0.2})
        self.assertIn("Source text", payload["messages"][1]["content"])
        post.return_value.raise_for_status.assert_called_once()

    @patch("app.llm_provider.requests.post")
    def test_bad_responses_are_rejected(self, post):
        provider = OllamaProvider("http://localhost:11434", "test-model")
        for body in [{}, [], {"error": "missing model"}, {"message": {}},
                     {"message": {"content": " "}}, {"message": {"content": 42}}]:
            with self.subTest(body=body):
                post.return_value.json.return_value = body
                with self.assertRaises(ValueError):
                    provider.summarize("Title", "Source text")

    @patch("app.llm_provider.requests.post")
    def test_http_error_is_not_parsed_as_summary(self, post):
        post.return_value.raise_for_status.side_effect = requests.HTTPError("404")
        with self.assertRaises(requests.HTTPError):
            OllamaProvider("http://localhost:11434", "missing").summarize("Title", "Text")
        post.return_value.json.assert_not_called()

    def test_factory_uses_environment_settings(self):
        with patch.multiple(settings, LLM_PROVIDER="ollama", LLM_MODEL="chosen-model",
                            LLM_BASE_URL="http://localhost:11434", LLM_TIMEOUT=33,
                            LLM_MAX_TOKENS=90, LLM_TEMPERATURE=0.4):
            provider = create_llm_provider()
        self.assertEqual(provider.model, "chosen-model")
        self.assertEqual(provider.timeout, 33)
        self.assertEqual(provider.max_tokens, 90)


class SummarizerTests(unittest.TestCase):
    def test_post_content_takes_priority_over_likes(self):
        provider = Mock()
        provider.summarize.return_value = "Summary."
        article = {"title": "Post", "description": "80 likes",
                   "content": "A new open model was released for local inference."}
        result = NewsSummarizer(provider).summarize_articles([article])
        provider.summarize.assert_called_once_with(article["title"], article["content"])
        self.assertEqual(result[0]["summary"], "Summary.")
        self.assertEqual(result[0]["content"], article["content"])

    def test_failures_fall_back_without_dropping_articles(self):
        for error in [requests.Timeout(), requests.ConnectionError(), ValueError("bad JSON")]:
            with self.subTest(error=type(error).__name__):
                provider = Mock()
                provider.summarize.side_effect = error
                text = "Long source description. " * 12
                result = NewsSummarizer(provider).summarize_articles([
                    {"title": "Story", "description": text}
                ])
                self.assertEqual(result[0]["summary"], text[:150])

    def test_short_and_missing_text_do_not_call_provider(self):
        provider = Mock()
        result = NewsSummarizer(provider).summarize_articles([
            {"title": "Short"}, {"title": None, "description": None}
        ])
        self.assertEqual([a["summary"] for a in result], ["Short", "No summary available"])
        provider.summarize.assert_not_called()


class ConfigurationTests(unittest.TestCase):
    def test_no_cloud_key_is_required(self):
        with patch.multiple(settings, NEWSAPI_KEY="test", EMAIL_SENDER="sender",
                            EMAIL_PASSWORD="password", EMAIL_RECIPIENT="recipient"):
            self.assertTrue(settings.validate_config())
        self.assertFalse(hasattr(settings, "OPENAI_API_KEY"))

    def test_news_key_is_required(self):
        with patch.object(settings, "NEWSAPI_KEY", ""):
            with self.assertRaisesRegex(ValueError, "NEWSAPI_KEY"):
                settings.validate_config()

    def test_invalid_local_settings_fail_early(self):
        cases = [("LLM_PROVIDER", "cloud"), ("LLM_BASE_URL", "file:///tmp/model"),
                 ("LLM_BASE_URL", "http://user:secret@localhost:11434"),
                 ("LLM_MODEL", ""), ("LLM_TIMEOUT", 0), ("LLM_TIMEOUT", float("nan")),
                 ("LLM_MAX_TOKENS", 0), ("LLM_TEMPERATURE", 3)]
        for name, value in cases:
            with self.subTest(setting=name), patch.object(settings, name, value):
                with self.assertRaises(ValueError):
                    settings.validate_llm_config()


class PipelineTests(unittest.TestCase):
    def test_pipeline_uses_configured_local_summarizer(self):
        # Import/startup succeeds without the optional scraper installed.
        from app import main

        with patch.object(main, "NewsFetcher") as fetcher, \
             patch.object(main, "get_hackernews_tech_stories", return_value=[]), \
             patch.object(main, "get_nitter_tweets", return_value=[]), \
             patch("app.summarizer.create_llm_provider") as factory, \
             patch.object(main, "EmailSender") as sender, \
             patch.object(main, "logger"):
            fetcher.return_value.fetch_ai_news.return_value = [
                {"title": "A local model", "description": "A new model runs entirely on personal computers."}
            ]
            fetcher.return_value.fetch_world_news.return_value = []
            factory.return_value.summarize.return_value = "Verified local summary."
            sender.return_value.send_news_email.return_value = True
            self.assertTrue(main.send_daily_news())
            factory.assert_called_once_with()
            factory.return_value.summarize.assert_called_once()
            sent = sender.return_value.send_news_email.call_args.kwargs
            self.assertEqual(sent["ai_news"][0]["summary"], "Verified local summary.")


if __name__ == "__main__":
    unittest.main()

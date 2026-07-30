import time

import requests
from bs4 import BeautifulSoup
from googlenewsdecoder import gnewsdecoder


class ArticleExtractor:
    """
    Resolves the real publisher URL behind a Google News RSS redirect
    link, then scrapes and cleans the article text.

    Google News RSS links (news.google.com/rss/articles/...) are not
    the actual article; fetching them directly just returns Google's
    client-side redirect shell page. gnewsdecoder() talks to Google's
    internal batchexecute endpoint to resolve the real URL first.
    """

    MIN_CONTENT_LENGTH = 200

    def __init__(self, decode_interval=1):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.decode_interval = decode_interval

    def _resolve_url(self, url):
        """Return the real article URL, or the original url on failure."""
        if not url or "news.google.com" not in url:
            return url

        try:
            result = gnewsdecoder(url, interval=self.decode_interval)
            if result.get("status") and result.get("decoded_url"):
                return result["decoded_url"]
        except Exception:
            pass

        # Couldn't decode -- return original so caller can still try
        # (and so callers can tell a decode failure from a scrape failure).
        return url

    def extract(self, article):
        raw_url = article.get("link", "")

        if not raw_url:
            article["content"] = ""
            return article

        resolved_url = self._resolve_url(raw_url)
        article["resolved_link"] = resolved_url

        try:
            response = requests.get(resolved_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            text = soup.get_text(separator=" ")
            text = " ".join(text.split())

            # If the resolve step silently failed, we're often still
            # sitting on a Google News shell page -- these are short
            # and just contain nav chrome, not article text.
            if len(text) < self.MIN_CONTENT_LENGTH:
                fallback = article.get("summary") or article.get("description") or ""
                fallback = " ".join(BeautifulSoup(fallback, "html.parser").get_text().split())
                if len(fallback) > len(text):
                    text = fallback
                    article["extraction_note"] = "used_rss_summary_fallback"

            article["content"] = text[:5000]

        except Exception as e:
            # Fall back to the RSS summary rather than storing an error
            # string as "content" -- that string used to get sent
            # straight into the LLM analyzer and the PDF report.
            fallback = article.get("summary") or article.get("description") or ""
            fallback = " ".join(BeautifulSoup(fallback, "html.parser").get_text().split()) if fallback else ""
            article["content"] = fallback
            article["extraction_note"] = f"scrape_failed: {e}"

        return article

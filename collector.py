import feedparser
import yaml
from urllib.parse import quote


class BatteryCollector:

    def __init__(self, keyword_file):
        with open(keyword_file, "r", encoding="utf-8") as file:
            self.keywords = yaml.safe_load(file)

    def create_search_url(self, keyword):
        encoded_keyword = quote(keyword)
        url = (
            "https://news.google.com/rss/search?q="
            + encoded_keyword
            + "&hl=en-US&gl=US&ceid=US:en"
        )
        return url

    def collect_articles(self):
        articles = []
        all_keywords = []

        for company_keywords in self.keywords["companies"].values():
            all_keywords.extend(company_keywords)

        for tech_keywords in self.keywords["technologies"].values():
            all_keywords.extend(tech_keywords)

        for keyword in all_keywords:
            print(f"Searching: {keyword}")

            url = self.create_search_url(keyword)
            feed = feedparser.parse(url)

            for item in feed.entries[:5]:
                article = {
                    "keyword": keyword,
                    "title": item.title,
                    "link": item.link,
                    "published": item.get("published", ""),
                    # RSS summary -- used as a fallback when the full
                    # article can't be scraped (paywall, decode failure,
                    # etc). Without this, article_extractor has nothing
                    # to fall back on.
                    "summary": item.get("summary", ""),
                    "source": item.get("source", {}).get("title", ""),
                }

                articles.append(article)

        return articles

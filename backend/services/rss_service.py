import hashlib
import re
from datetime import datetime
from typing import List, Dict

import feedparser

RSS_FEEDS = [
    {"name": "Google AI Blog", "url": "https://blog.google/technology/ai/rss/"},
    {"name": "DeepMind", "url": "https://deepmind.google/blog/rss.xml"},
    {"name": "Hugging Face", "url": "https://huggingface.co/blog/feed.xml"},
    {"name": "The Gradient", "url": "https://thegradient.pub/rss/"},
    {"name": "Ars Technica AI", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
]

# Per-feed article limit to control embedding cost
ARTICLES_PER_FEED = 15


def _strip_html(raw: str) -> str:
    clean = re.sub(r"<[^>]+>", " ", raw)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


def fetch_all_articles() -> List[Dict]:
    articles = []
    seen_ids: set = set()

    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            count = 0
            for entry in feed.entries:
                if count >= ARTICLES_PER_FEED:
                    break

                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                if not title or not link:
                    continue

                raw_summary = entry.get("summary", entry.get("description", ""))
                summary = _strip_html(raw_summary)[:1000]
                published = entry.get("published", str(datetime.utcnow()))

                # Stable dedup ID from URL
                article_id = hashlib.md5(link.encode()).hexdigest()
                if article_id in seen_ids:
                    continue
                seen_ids.add(article_id)

                # Text field is what gets embedded and stored as ChromaDB document
                text = f"{title}\n\n{summary}"

                articles.append(
                    {
                        "id": article_id,
                        "title": title,
                        "text": text,
                        "url": link,
                        "source": feed_info["name"],
                        "published": published,
                    }
                )
                count += 1

        except Exception as e:
            print(f"[RSS] Failed to fetch {feed_info['name']}: {e}")

    print(f"[RSS] Fetched {len(articles)} articles from {len(RSS_FEEDS)} feeds")
    return articles

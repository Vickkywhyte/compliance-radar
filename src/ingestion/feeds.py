import logging

import feedparser

logger = logging.getLogger(__name__)


def fetch_rss_feed(feed_url: str) -> list[dict]:
    """Fetch and parse an RSS feed, returning a list of article dicts.

    Returns:
        list[dict]: Each dict contains 'title', 'link', 'published', 'raw_text'.
    """
    try:
        feed = feedparser.parse(feed_url)
    except Exception:
        logger.exception("Failed to fetch RSS feed: %s", feed_url)
        return []

    if feed.bozo and not feed.entries:
        logger.warning(
            "Malformed feed with no entries: %s (error: %s)",
            feed_url,
            feed.bozo_exception,
        )
        return []

    articles: list[dict] = []
    for entry in feed.entries:
        content_blocks = entry.get("content", [])
        raw_text = (
            content_blocks[0].get("value", "") if content_blocks
            else entry.get("summary", "")
        )

        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "raw_text": raw_text,
        })

    logger.info("Fetched %d articles from %s", len(articles), feed_url)
    return articles

import logging
import time

from src.ai.processor import process_article
from src.database import check_exists, insert_event
from src.ingestion.feeds import fetch_rss_feed

logger = logging.getLogger(__name__)

TARGET_FEEDS: list[str] = [
    # Global
    "https://www.fatf-gafi.org/content/fatf-gafi/en/publications.rss",
    # United States
    "https://www.fincen.gov/news/news-releases/rss.xml",
    "https://ofac.treasury.gov/recent-actions/rss.xml",
    # United Kingdom
    "https://www.fca.org.uk/news/rss.xml",
    # European Union
    "https://www.amla.europa.eu/node/19/rss_en",
    "https://www.eba.europa.eu/news-press/news/rss.xml",
]


def run_pipeline() -> dict:
    """Run the full ingestion pipeline across all target feeds.

    Returns:
        dict: Summary with keys 'found', 'skipped', 'inserted', 'errors'.
    """
    stats = {"found": 0, "skipped": 0, "inserted": 0, "errors": 0}

    for feed_url in TARGET_FEEDS:
        logger.info("Processing feed: %s", feed_url)
        articles = fetch_rss_feed(feed_url)

        for article in articles:
            stats["found"] += 1
            url = article["link"]
            title = article["title"]

            if not url:
                logger.warning("Skipping article with no URL: %s", title)
                stats["skipped"] += 1
                continue

            if check_exists(url):
                logger.debug("Duplicate, skipping: %s", url)
                stats["skipped"] += 1
                continue

            try:
                raw_text = article["raw_text"]
                if not raw_text:
                    logger.warning("No text content for: %s", url)
                    stats["skipped"] += 1
                    continue

                event = process_article(raw_text=raw_text, url=url)
                insert_event(event)
                stats["inserted"] += 1
                logger.info("Inserted: %s", title)
                time.sleep(4.5)

            except Exception:
                logger.exception("Failed to process article: %s", url)
                stats["errors"] += 1

    logger.info(
        "Pipeline complete — Found: %d | Skipped: %d | Inserted: %d | Errors: %d",
        stats["found"],
        stats["skipped"],
        stats["inserted"],
        stats["errors"],
    )
    return stats


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    run_pipeline()

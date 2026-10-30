import io
import logging

import feedparser
import httpx
import pdfplumber

logger = logging.getLogger(__name__)

PDF_DOWNLOAD_TIMEOUT = 30


def extract_text_from_pdf(pdf_url: str) -> str:
    """Download a PDF from a URL and extract its text. Returns empty string on failure."""
    try:
        response = httpx.get(pdf_url, timeout=PDF_DOWNLOAD_TIMEOUT, follow_redirects=True)
        response.raise_for_status()
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages).strip()
    except Exception:
        logger.exception("Failed to extract text from PDF: %s", pdf_url)
        return ""


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
        link = entry.get("link", "")
        title = entry.get("title", "")
        published = entry.get("published", "")

        if link.lower().endswith(".pdf"):
            raw_text = extract_text_from_pdf(link)
            if not raw_text:
                logger.warning("Skipping PDF with no extractable text: %s", link)
                continue
        else:
            content_blocks = entry.get("content", [])
            raw_text = (
                content_blocks[0].get("value", "") if content_blocks
                else entry.get("summary", "")
            )

        articles.append({
            "title": title,
            "link": link,
            "published": published,
            "raw_text": raw_text,
        })

    logger.info("Fetched %d articles from %s", len(articles), feed_url)
    return articles

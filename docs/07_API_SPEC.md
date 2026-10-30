# Internal API Spec (Module Contracts)

This document defines the function signatures and expected inputs/outputs for our core Python modules. This ensures that the Ingestion module, AI module, and Database module can be built independently without integration issues.

## 1. Ingestion Module (`src/ingestion/feeds.py`)

```python
def fetch_rss_feed(feed_url: str) -> list[dict]:
    """
    Fetches and parses an RSS feed.
    
    Args:
        feed_url (str): The URL of the RSS feed.
        
    Returns:
        list[dict]: A list of dictionaries, each containing:
            - 'title' (str)
            - 'link' (str)
            - 'published' (str)
            - 'raw_text' (str)
    """
import logging
import os
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client

from src.models import ComplianceEvent

load_dotenv()

logger = logging.getLogger(__name__)

TABLE_NAME = "compliance_events"


def _get_secret(key: str) -> Optional[str]:
    """Read a secret from st.secrets (Streamlit Cloud) or os.getenv (local/.env)."""
    try:
        import streamlit as st
        return st.secrets.get(key)
    except (ImportError, AttributeError, FileNotFoundError):
        return os.getenv(key)


def get_supabase_client() -> Client:
    url = _get_secret("SUPABASE_URL")
    key = _get_secret("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_KEY must be set in .env or Streamlit secrets."
        )
    return create_client(url, key)


def check_exists(url: str) -> bool:
    """Check if a compliance event with the given source URL already exists."""
    try:
        client = get_supabase_client()
        result = (
            client.table(TABLE_NAME)
            .select("id")
            .eq("source_url", url)
            .execute()
        )
        return len(result.data) > 0
    except Exception:
        logger.exception("Failed to check existence for URL: %s", url)
        raise


def insert_event(event: ComplianceEvent) -> dict:
    """Insert a validated ComplianceEvent into the database and return the new row."""
    try:
        client = get_supabase_client()
        payload = event.model_dump(mode="json")
        result = (
            client.table(TABLE_NAME)
            .insert(payload)
            .execute()
        )
        return result.data[0]
    except Exception:
        logger.exception("Failed to insert event: %s", event.title)
        raise

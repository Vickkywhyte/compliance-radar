import logging
import os
from typing import Optional

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

from src.models import ComplianceEvent

load_dotenv()

logger = logging.getLogger(__name__)


def _get_secret(key: str) -> Optional[str]:
    """Read a secret from st.secrets (Streamlit Cloud) or os.getenv (local/.env)."""
    try:
        import streamlit as st
        return st.secrets.get(key)
    except (ImportError, AttributeError, FileNotFoundError):
        return os.getenv(key)


def get_connection() -> psycopg2.extensions.connection:
    """Open a connection to the Neon PostgreSQL database."""
    dsn = _get_secret("DATABASE_URL")
    if not dsn:
        raise EnvironmentError("DATABASE_URL must be set in .env or Streamlit secrets.")
    return psycopg2.connect(dsn)


def check_exists(url: str) -> bool:
    """Check if a compliance event with the given source URL already exists."""
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM compliance_events WHERE source_url = %s LIMIT 1",
                    (url,),
                )
                return cur.fetchone() is not None
        conn.close()
    except Exception:
        logger.exception("Failed to check existence for URL: %s", url)
        raise


def insert_event(event: ComplianceEvent) -> dict:
    """Insert a validated ComplianceEvent and return the new row as a dict."""
    try:
        payload = event.model_dump(mode="json")
        columns = list(payload.keys())
        values = [payload[c] for c in columns]
        col_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        conn = get_connection()
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"INSERT INTO compliance_events ({col_str}) VALUES ({placeholders}) RETURNING *",
                    values,
                )
                row = cur.fetchone()
        conn.close()
        return dict(row)
    except Exception:
        logger.exception("Failed to insert event: %s", event.title)
        raise


def fetch_all_events() -> list[dict]:
    """Fetch all compliance events ordered by created_at descending."""
    conn = get_connection()
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM compliance_events ORDER BY created_at DESC")
            rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_latest_event_timestamp() -> Optional[str]:
    """Return the created_at of the most recent event, or None."""
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT created_at FROM compliance_events ORDER BY created_at DESC LIMIT 1"
            )
            row = cur.fetchone()
    conn.close()
    return str(row[0]) if row else None


def update_event_triage(event_id: str, changes: dict) -> None:
    """Update triage fields for a single event by id."""
    set_clause = ", ".join(f"{k} = %s" for k in changes)
    values = list(changes.values()) + [event_id]
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE compliance_events SET {set_clause} WHERE id = %s",
                values,
            )
    conn.close()


def insert_subscriber(email: str) -> None:
    """Insert a new subscriber email. Raises on duplicate."""
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO subscribers (email) VALUES (%s)",
                (email,),
            )
    conn.close()


def get_active_subscriber_emails() -> list[str]:
    """Return emails of all active subscribers."""
    conn = get_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email FROM subscribers WHERE is_active = TRUE")
            rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def fetch_digest_events(cutoff_iso: str) -> list[dict]:
    """Fetch top 3 unread high-relevance events since the cutoff timestamp."""
    conn = get_connection()
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """SELECT title, jurisdiction, relevance_score, source_url, summary
                   FROM compliance_events
                   WHERE created_at >= %s
                     AND relevance_score >= 7
                     AND triage_status = 'Unread'
                   ORDER BY relevance_score DESC
                   LIMIT 3""",
                (cutoff_iso,),
            )
            rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

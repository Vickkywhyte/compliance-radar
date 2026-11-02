import logging
import os
from datetime import datetime, timedelta, timezone

import resend
from dotenv import load_dotenv

from src.database import get_supabase_client

load_dotenv()

logger = logging.getLogger(__name__)

TABLE_NAME = "compliance_events"


def _build_html(events: list[dict]) -> str:
    """Build a styled HTML email body from a list of event dicts."""
    rows = ""
    for ev in events:
        score = ev.get("relevance_score", "?")
        rows += f"""
        <tr>
          <td style="padding:12px;border-bottom:1px solid #e0e0e0;">
            <a href="{ev.get('source_url', '#')}" style="color:#1a73e8;text-decoration:none;font-weight:600;">
              {ev.get('title', 'Untitled')}
            </a>
            <br>
            <span style="color:#666;font-size:13px;">
              {ev.get('jurisdiction', 'Unknown')} &middot; Score: {score}/10
            </span>
          </td>
        </tr>"""

    return f"""
    <div style="font-family:Arial,Helvetica,sans-serif;max-width:600px;margin:0 auto;color:#222;">
      <div style="background:#0d1b2a;padding:20px;text-align:center;">
        <h1 style="color:#fff;margin:0;font-size:22px;">Global Compliance Radar</h1>
        <p style="color:#8eafc5;margin:4px 0 0;font-size:14px;">Daily Briefing</p>
      </div>
      <div style="padding:20px;">
        <p style="font-size:14px;">The following high-priority regulatory events were ingested in the last 24 hours:</p>
        <table style="width:100%;border-collapse:collapse;">
          {rows}
        </table>
        <p style="font-size:12px;color:#999;margin-top:20px;">
          This is an automated digest. Do not reply to this email.
        </p>
      </div>
    </div>"""


def send_daily_digest() -> None:
    """Query top unread high-relevance events from the last 24h and email a digest."""
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        logger.warning("RESEND_API_KEY not set, skipping daily digest.")
        return

    recipient = os.getenv("DIGEST_EMAIL_TO")
    if not recipient:
        logger.warning("DIGEST_EMAIL_TO not set, skipping daily digest.")
        return

    resend.api_key = api_key

    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

    try:
        client = get_supabase_client()
        result = (
            client.table(TABLE_NAME)
            .select("title, jurisdiction, relevance_score, source_url")
            .gte("created_at", cutoff)
            .gte("relevance_score", 7)
            .eq("triage_status", "Unread")
            .order("relevance_score", desc=True)
            .limit(3)
            .execute()
        )
    except Exception:
        logger.exception("Failed to query events for daily digest.")
        return

    events = result.data
    if not events:
        logger.info("No high-relevance unread events in the last 24h. Skipping digest.")
        return

    html_body = _build_html(events)

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [recipient],
            "subject": f"Compliance Radar Briefing — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            "html": html_body,
        })
        logger.info("Daily digest sent to %s with %d events.", recipient, len(events))
    except Exception:
        logger.exception("Failed to send daily digest email.")

import logging
import os
from datetime import datetime, timedelta, timezone

from brevo import Brevo
from dotenv import load_dotenv

from src.database import fetch_digest_events, get_active_subscriber_emails

load_dotenv()

logger = logging.getLogger(__name__)


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
            <p style="color:#444;font-size:13px;line-height:1.5;margin:6px 0 0;">
              {ev.get('summary', '')}
            </p>
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


def _get_subscriber_emails() -> list[str]:
    """Fetch active subscriber emails from the database, falling back to env var."""
    try:
        emails = get_active_subscriber_emails()
        if emails:
            return emails
    except Exception:
        logger.exception("Failed to query subscribers table.")

    fallback = os.getenv("DIGEST_EMAIL_TO")
    if fallback:
        logger.info("No active subscribers found. Using DIGEST_EMAIL_TO fallback.")
        return [fallback]
    return []


def send_daily_digest() -> None:
    """Query top unread high-relevance events from the last 24h and email a digest via Brevo."""
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        logger.warning("BREVO_API_KEY not set, skipping daily digest.")
        return

    sender_email = os.getenv("BREVO_SENDER_EMAIL")
    if not sender_email:
        logger.warning("BREVO_SENDER_EMAIL not set, skipping daily digest.")
        return

    recipients = _get_subscriber_emails()
    if not recipients:
        logger.warning("No subscribers and DIGEST_EMAIL_TO not set. Skipping digest.")
        return

    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

    try:
        events = fetch_digest_events(cutoff)
    except Exception:
        logger.exception("Failed to query events for daily digest.")
        return

    if not events:
        logger.info("No high-relevance unread events in the last 24h. Skipping digest.")
        return

    html_body = _build_html(events)
    subject = f"Compliance Radar Briefing — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"

    brevo_client = Brevo(api_key=api_key)

    try:
        brevo_client.transactional_emails.send_transac_email(
            sender={"email": sender_email, "name": "Global Compliance Radar"},
            to=[{"email": sender_email}],
            bcc=[{"email": email} for email in recipients],
            subject=subject,
            html_content=html_body,
        )
        logger.info("Daily digest sent to %d subscribers with %d events.", len(recipients), len(events))
    except Exception:
        logger.exception("Failed to send daily digest via Brevo.")

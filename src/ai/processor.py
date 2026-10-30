import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import HttpUrl, ValidationError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.models import ComplianceEvent

load_dotenv()

logger = logging.getLogger(__name__)


class _ThoughtSignatureFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "non-text parts in the response: ['thought_signature']" not in record.getMessage()


# Gemini 3 responses include a thought_signature part; the SDK warns on every call even though the JSON parses fine.
logging.getLogger("google_genai.types").addFilter(_ThoughtSignatureFilter())

GEMINI_MODEL = "gemini-3.1-flash-lite"

SYSTEM_PROMPT = """\
You are a compliance intelligence analyst specializing in AML/CFT regulations.
Analyze the provided article text and extract structured data.

## Relevance Scoring Rubric (1-10)
- 10 (Critical): Global standard changes (e.g., FATF Recommendations update), \
massive sanctions packages (e.g., new OFAC SDN list additions affecting major banks), \
or systemic enforcement actions.
- 8-9 (High): Major regional regulations (EU AMLR, US BSA updates) or high-profile \
fines against tier-1 banks.
- 5-7 (Medium): Jurisdiction-specific guidance, thematic reviews by regulators \
(e.g., FCA "Dear CEO" letters), or emerging typologies.
- 1-4 (Low): Niche local regulations, routine speeches, or general news commentary \
with no immediate compliance impact.

## Status Classification Rules
- Proposed: Draft legislation, consultation papers, or upcoming rules not yet finalized.
- In Force: Final rules, acts, or directives currently active.
- Enforcement: Fines, settlements, prosecutions, or regulatory bans.
- Guidance: Advisory notices, typology reports, FAQs, or "Dear CEO" letters.

## Critical Rules
- For source_url: you MUST use EXACTLY the URL provided in the user prompt. \
Do NOT generate, modify, or hallucinate any URL.
- If the text does not contain enough information to determine the effective date, \
return null. Do not guess.
- The summary must be exactly 2 sentences.
- The recommended_action must be a specific, actionable next step for a compliance officer."""


@retry(
    retry=retry_if_exception_type(genai_errors.ServerError),
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def _call_gemini(client: genai.Client, user_prompt: str) -> str:
    """Call Gemini with retries on transient server errors. Returns raw JSON text."""
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComplianceEvent,
            system_instruction=SYSTEM_PROMPT,
            http_options=types.HttpOptions(timeout=60_000),
        ),
    )
    return response.text


def process_article(raw_text: str, url: str) -> ComplianceEvent:
    """Analyze raw article text with Gemini and return a structured ComplianceEvent."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY must be set in the .env file.")

    client = genai.Client(api_key=api_key)

    user_prompt = (
        f"The source URL for this article is exactly: {url}\n\n"
        f"Analyze the following article:\n\n{raw_text}"
    )

    try:
        response_text = _call_gemini(client, user_prompt)
    except genai_errors.ServerError:
        logger.exception("Gemini API still unavailable after retries for URL: %s", url)
        raise
    except Exception:
        logger.exception("Gemini API call failed for URL: %s", url)
        raise

    try:
        event = ComplianceEvent.model_validate_json(response_text)
    except ValidationError:
        logger.exception(
            "Pydantic validation failed for Gemini response. URL: %s, Response (truncated): %.500s",
            url,
            response_text,
        )
        raise

    # Defense-in-depth: override source_url to guarantee it matches the
    # actual input, per eval spec §5 hallucination guardrails.
    event = event.model_copy(update={"source_url": HttpUrl(url)})

    return event

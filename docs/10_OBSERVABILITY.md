# Observability (Logging & Metrics)

## 1. Philosophy
If a cron job fails silently in a GitHub Action at 3:00 AM, we need to know why without digging through raw terminal output. We must implement structured logging and basic metrics.

## 2. Logging Strategy
We will use Python's built-in `logging` module (no external paid tools like Datadog for the MVP).

- **Format:** JSON format is preferred for logs so they can be easily parsed later.
- **Levels:**
  - `INFO`: Pipeline started, RSS feed fetched (X items), LLM processed article, Database insert successful.
  - `WARNING`: A specific RSS feed timed out, or an article was skipped due to missing text.
  - `ERROR`: Gemini API limit reached, Supabase connection failed, Pydantic validation failed.
- **Location:** Logs will be printed to `stdout` so they are captured by GitHub Actions and visible in the action run history.

## 3. Metrics to Track (MVP)
We will log a summary at the end of every pipeline run:
- Total articles found across all feeds.
- Total articles skipped (duplicates).
- Total articles successfully processed and inserted.
- Total tokens used by Gemini (to monitor free tier limits).
- Execution time (start to finish).

## 4. Alerting
For the MVP, GitHub Actions' built-in failure notifications will suffice. If the cron job fails, GitHub will email the repo owner. Future iterations can integrate a webhook to Slack/Discord.
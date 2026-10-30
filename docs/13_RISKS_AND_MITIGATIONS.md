# Risks and Mitigations

A senior engineer anticipates what could go wrong before writing code. This document outlines the known risks for the Global Compliance Radar and how we will mitigate them.

## 1. Technical Risks

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **API Rate Limits** (Gemini Free Tier) | High | Medium | Implement exponential backoff. If we hit the limit, the script sleeps and retries. Cache processed URLs so we never process the same article twice. |
| **Scraping Blocks / Feed Changes** | Medium | High | Stick to official RSS feeds instead of scraping HTML. Add try/except blocks so one broken feed doesn't crash the whole pipeline. |
| **LLM Hallucinations** (Fake info) | High | Medium | Use strict Pydantic schema validation. Force the AI to return `null` if it doesn't know the effective date. Do not let the AI generate the `source_url`. |
| **Database Downtime** (Supabase) | Medium | Low | The pipeline will fail gracefully, log the error, and the next daily cron job will catch the missed articles. |

## 2. Product Risks

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Information Overload** (Too many low-quality items) | High | High | The 1-10 Relevance Score. The UI will default to showing only items with a score of 5 or higher. |
| **Jurisdictional Bias** | Medium | Medium | Ensure the initial RSS feeds cover Global (FATF), US, UK, and EU. Allow users to filter by jurisdiction. |

## 3. Compliance/Business Risks

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Reliance on AI as Legal Advice** | High | Medium | The UI must include a disclaimer: *"This is an automated intelligence tool, not legal advice. Always verify against the primary source."* |
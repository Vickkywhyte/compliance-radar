# Security & Privacy

## 1. Secrets Management
- **NEVER** commit API keys to Git.
- All secrets (Supabase URL, Supabase Anon Key, Gemini API Key) must be stored in a `.env` file locally.
- The `.env` file must be added to `.gitignore`.
- In production (GitHub Actions), secrets will be stored in GitHub Repository Secrets and injected into the environment variables at runtime.

## 2. Database Security
- **Supabase RLS (Row Level Security):** For the MVP, the database will be accessed via the `service_role` key only by the backend pipeline (GitHub Actions). The Streamlit UI will use the `anon` key, which will have **Read-Only** access to the `compliance_events` table. Users cannot modify or delete records from the UI.
- No PII (Personally Identifiable Information) will be stored in the database. We are only storing public regulatory data.

## 3. AI Data Privacy
- We are sending publicly available regulatory text to Google Gemini. No proprietary bank data, customer data, or internal compliance documents will be sent to the LLM.
- We will review Google's API data usage policy to ensure our inputs are not used to train their public models (standard for the paid API, but we must verify for the free tier).
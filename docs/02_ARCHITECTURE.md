# Architecture Decision Records (ADRs)

## ADR 001: Database - Supabase over Firebase
- **Status:** Accepted
- **Context:** We need a database for structured compliance data with a free tier and easy Python integration.
- **Decision:** Use Supabase (PostgreSQL).
- **Rationale:** Compliance data is inherently relational (e.g., Sources, Events, Jurisdictions). PostgreSQL is the industry standard for relational data. Supabase provides a generous free tier, an auto-generated REST API, and a native Python client. Firebase (NoSQL) would make complex querying and future relational mapping (e.g., linking Events to specific Tags) much harder.

## ADR 002: AI Engine - Google Gemini 1.5 Flash
- **Status:** Accepted
- **Context:** We need an LLM that can process large text documents, output strict JSON, and operate within a zero-cost budget.
- **Decision:** Use Google Gemini 1.5 Flash via the free API tier.
- **Rationale:** Gemini 1.5 Flash has a massive context window (ideal for long regulatory PDFs/HTML), supports native structured JSON output schemas, and currently offers a highly generous free tier (15 RPM / 1M TPM). OpenAI's GPT-4o is too expensive; local models (Ollama) require local compute and don't scale to cloud deployment for free.

## ADR 003: Backend Orchestration - GitHub Actions
- **Status:** Accepted
- **Context:** We need a way to run the ingestion and AI scripts daily without paying for a server (EC2, DigitalOcean, etc.).
- **Decision:** Use GitHub Actions with a cron schedule.
- **Rationale:** GitHub Actions provides 2,000 free minutes per month for private repos (unlimited for public). A daily script that runs for 5 minutes uses ~150 minutes a month. This fits perfectly within the free tier and provides excellent logging and failure notifications out of the box.

## ADR 004: Frontend - Streamlit
- **Status:** Accepted
- **Context:** We need a fast, Python-based UI to display the dashboard without writing HTML/CSS/React.
- **Decision:** Use Streamlit.
- **Rationale:** The developer is working in Python. Streamlit allows building interactive dashboards in pure Python. It deploys for free on Streamlit Community Cloud. If the product scales, the UI can be rewritten in React/Next.js without touching the backend.
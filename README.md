# Global Compliance Radar

An automated, AI-driven intelligence platform that ingests global AML/CFT regulatory updates and transforms them into structured, actionable compliance briefings.

**[View Live Dashboard](https://compliance-radar-xaajzx2r9qnytpxkuhvrr5.streamlit.app/)**

## Features

- **AI-Driven Scoring & Classification** -- Every regulatory update is analyzed by Google Gemini and assigned a relevance score (1--10), jurisdiction, status, and a recommended action for compliance officers.
- **Automated Multi-Source Ingestion** -- RSS and PDF sources from FATF, FinCEN, OFAC, FCA, AMLA, and EBA are fetched daily, deduplicated, and stored automatically.
- **Interactive Streamlit Dashboard** -- Filter events by relevance score, jurisdiction, and status. Every item links back to the original source for full provenance.
- **Interactive Triage Workflow** -- Assign events to team members and update their triage status (Unread, In Review, Actioned, Dismissed) directly from the dashboard. All changes persist to the database instantly.

## Open Core Model

Global Compliance Radar follows an **Open Core** model. The Community Edition is free, open-source, and licensed under MIT. An Enterprise Edition is planned for teams that need multi-tenant capabilities and deeper integrations.

| | Community (Free) | Enterprise (Planned) |
|:--|:-----------------|:---------------------|
| Core ingestion engine | Included | Included |
| AI scoring & classification | Included | Included |
| Public dashboard | Included | Included |
| Multi-tenant auth & RLS | -- | Included |
| Custom RSS / PDF feeds | -- | Included |
| Automated audit logs | -- | Included |
| Slack / Teams webhook alerts | -- | Included |

The Community Edition is fully functional on its own. Enterprise features will be developed in a separate, licensed module that extends the open-source core without forking it.

## Tech Stack

| Layer | Technology |
|:------|:-----------|
| Language | Python 3.9+ |
| AI Engine | Google Gemini (via `google-genai` SDK) |
| Database | Supabase (PostgreSQL) |
| Frontend | Streamlit |
| Automation | GitHub Actions (daily cron) |
| Validation | Pydantic v2 |

## Project Structure

```
src/
  models.py              # Pydantic data models
  database.py            # Supabase client & queries
  ai/
    processor.py         # Gemini structured output pipeline
  ingestion/
    feeds.py             # RSS & PDF feed parser
    pipeline.py          # Main orchestrator
  ui/
    app.py               # Streamlit dashboard
docs/                    # Architecture, PRD, data model, etc.
.github/workflows/
  daily_run.yml          # Scheduled GitHub Action
```

## Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Vickkywhyte/compliance-radar.git
   cd compliance-radar
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:

   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

4. **Run the ingestion pipeline**

   ```bash
   python -m src.ingestion.pipeline
   ```

5. **Launch the dashboard**

   ```bash
   streamlit run src/ui/app.py
   ```

## Deployment

- **Backend pipeline** runs daily at 6:00 AM UTC via GitHub Actions (`.github/workflows/daily_run.yml`). Secrets are injected from GitHub Repository Secrets.
- **Frontend dashboard** deploys automatically to Streamlit Community Cloud on push to `main`. Supabase credentials are configured in the Streamlit Secrets manager.

See `docs/12_DEPLOYMENT.md` for the full deployment guide.

## Enterprise Roadmap

The architecture is designed to scale into a multi-tenant SaaS without rewriting the core:

1. **Tenant isolation** -- Add a `tenant_id` column to `compliance_events` and enforce row-level security (RLS) policies in Supabase so each organization sees only its own data.
2. **Authentication** -- Integrate Supabase Auth to support email/password and SSO login, with role-based access (analyst, manager, admin).
3. **Custom feeds** -- Allow each tenant to configure their own RSS/PDF sources via a `tenant_feeds` table, ingested on their own schedule.
4. **Audit logging** -- Record every pipeline run, user action, and data access event to a dedicated `audit_log` table for compliance reporting.
5. **Real-time alerts** -- Webhook integrations for Slack and Microsoft Teams, triggered when a new event exceeds a configurable relevance threshold.

## Contributing

Contributions are welcome. To get started:

1. **Fork** the repository.
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes.** Follow the coding standards in `CLAUDE.md` (type hints, Pydantic models, logging, no hardcoded secrets).
4. **Write tests** for any new functionality in the `tests/` directory.
5. **Submit a pull request** against `main` with a clear description of what you changed and why.

Please open an issue first if you're planning a large change so we can discuss the approach.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

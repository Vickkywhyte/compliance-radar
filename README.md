# Global Compliance Radar

An automated, AI-driven intelligence platform that ingests global AML/CFT regulatory updates and transforms them into structured, actionable compliance briefings.

**[View Live Dashboard](https://compliance-radar-xaajzx2r9qnytpxkuhvrr5.streamlit.app/)** *(update URL after deployment)*

## Features

- **AI-Driven Scoring & Classification** -- Every regulatory update is analyzed by Google Gemini and assigned a relevance score (1--10), jurisdiction, status, and a recommended action for compliance officers.
- **Automated Multi-Source Ingestion** -- RSS feeds from FATF, FinCEN, OFAC, and FCA are fetched daily, deduplicated, and stored automatically.
- **Interactive Streamlit Dashboard** -- Filter events by relevance score, jurisdiction, and status. Every item links back to the original source for full provenance.

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
    feeds.py             # RSS feed parser
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

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

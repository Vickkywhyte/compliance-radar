# Deployment Strategy

## 1. Local Development
- Developer runs the pipeline manually: `python -m src.ingestion.pipeline`
- Developer runs the UI locally: `streamlit run src/ui/app.py`
- Uses a local `.env` file for secrets.

## 2. Production Deployment (Zero-Cost Architecture)

### A. Backend Pipeline (Ingestion + AI)
- **Platform:** GitHub Actions.
- **Trigger:** Cron schedule (e.g., `0 6 * * *` for 6:00 AM UTC daily).
- **Workflow File:** `.github/workflows/daily_run.yml`
- **Steps:**
  1. Checkout code.
  2. Set up Python 3.11.
  3. Install dependencies (`pip install -r requirements.txt`).
  4. Run the pipeline script (Secrets injected via GitHub Secrets).

### B. Frontend Dashboard
- **Platform:** Streamlit Community Cloud.
- **Trigger:** Automatic deployment on push to the `main` branch.
- **Configuration:** Link the GitHub repo, set the main file path to `src/ui/app.py`, and add the Supabase `URL` and `anon key` to the Streamlit Secrets manager.

## 3. Rollback Strategy
If a bad deployment breaks the UI, Streamlit Community Cloud allows reverting to a previous commit in the dashboard. For the backend, if a pipeline update breaks the script, we revert the commit in GitHub, and the next cron run will use the stable code.
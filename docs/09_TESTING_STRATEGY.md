# Testing Strategy

## 1. Philosophy
In a zero-cost, AI-driven pipeline, we cannot manually review every output. Testing must be automated and run *before* code is pushed to production (or before the daily cron job runs). We follow the "Testing Pyramid": heavy on fast unit tests, lighter on integration tests.

## 2. Unit Tests (Fast, Isolated)
We will use `pytest` to test individual functions without hitting external APIs or databases.
- **Data Validation Tests:** Test that the Pydantic `ComplianceEvent` model rejects invalid data (e.g., a `relevance_score` of 11, or an invalid `status` string).
- **Prompt Construction Tests:** Test that the function building the LLM prompt correctly injects the raw text and the source URL.
- **Mocking:** We will use `unittest.mock` to mock the Gemini API response and the Supabase client so tests run in milliseconds without costing money or requiring internet.

## 3. Integration Tests (Slower, Connected)
These tests check if the modules work together. We will run these manually or in a separate GitHub Action before deployment.
- **Database Connectivity:** Test that the Python script can successfully connect to Supabase and insert a dummy record, then delete it.
- **LLM API Connectivity:** Test a single, real API call to Gemini to ensure the API key is valid and the model is responding.

## 4. Evaluation Tests (The "Golden Dataset")
As defined in `06_EVAL_SPEC.md`, we will write a script (`tests/test_eval.py`) that:
1. Loads `golden_dataset.json`.
2. Passes each article through the real AI processor.
3. Asserts that the AI's `jurisdiction`, `status`, and `relevance_score` match the human-verified scores. 
4. **Crucial:** If the LLM changes behavior (e.g., Gemini updates their model), this test will fail, alerting us that our prompt needs tuning.
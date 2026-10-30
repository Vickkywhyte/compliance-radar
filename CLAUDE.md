# CLAUDE.md - AI Assistant Rules

You are acting as a Senior Software Engineer assisting in the development of the **Global Compliance Radar**.

## 1. Project Context
- **Goal:** Build an automated, AI-driven intelligence platform that ingests global AML/CFT regulatory updates and transforms them into structured, actionable compliance briefings.
- **Architecture:** Modular Monolith.
- **Stack:** Python 3.11+, Streamlit (UI), Supabase/PostgreSQL (DB), Google Gemini (LLM), GitHub Actions (Cron).

## 2. The "Source of Truth"
Before writing or modifying any code, you MUST consult the documentation in the root folder.
- For product requirements: read `01_PRD.md`
- For system design: read `02_ARCHITECTURE.md`
- For data shapes: read `05_DATA_MODEL.md`
- For function signatures: read `07_API_SPEC.md`

## 3. Engineering Standards (How you must write code)
- **Type Hinting:** All Python functions must have strict type hints (e.g., `def foo(bar: str) -> int:`).
- **Pydantic:** Use Pydantic models for all data validation. Never pass raw dictionaries between modules.
- **Error Handling:** Use `try/except` blocks around external API calls (RSS feeds, Gemini, Supabase). Use the `logging` module; do not use `print()`.
- **Modularity:** Keep files small and focused. Do not write 500-line files. Extract logic into helper functions.
- **Testing:** If you write a complex function, write a corresponding `pytest` unit test in the `/tests` folder.

## 4. Constraints
- **Zero-Cost:** Do not suggest paid APIs or paid infrastructure. We are strictly on free tiers.
- **Security:** Never hardcode API keys. Always use `os.getenv()` loaded via `python-dotenv`.

## 5. Workflow
When asked to implement a feature:
1. Read the relevant docs.
2. Explain your plan.
3. Write the code.
4. Write the tests.
5. Provide instructions on how to run it locally.

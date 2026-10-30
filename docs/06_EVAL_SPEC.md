
---

### File 7: `06_EVAL_SPEC.md`

```markdown
# Evaluation Specification (Eval Spec)

## 1. Purpose
To ensure the LLM (Gemini) consistently outputs accurate, structured, and actionable intelligence. We cannot manually review every article, so we must define strict rubrics for the AI and build automated tests to catch hallucinations or schema failures.

## 2. The Relevance Scoring Rubric (1-10)
The LLM must use this exact rubric to assign the `relevance_score`:
*   **10 (Critical):** Global standard changes (e.g., FATF Recommendations update), massive sanctions packages (e.g., new OFAC SDN list additions affecting major banks), or systemic enforcement actions.
*   **8-9 (High):** Major regional regulations (EU AMLR, US BSA updates) or high-profile fines against tier-1 banks.
*   **5-7 (Medium):** Jurisdiction-specific guidance, thematic reviews by regulators (e.g., FCA "Dear CEO" letters), or emerging typologies.
*   **1-4 (Low):** Niche local regulations, routine speeches, or general news commentary with no immediate compliance impact.

## 3. Status Classification Rules
*   **Proposed:** Draft legislation, consultation papers, or upcoming rules not yet finalized.
*   **In Force:** Final rules, acts, or directives currently active.
*   **Enforcement:** Fines, settlements, prosecutions, or regulatory bans.
*   **Guidance:** Advisory notices, typology reports, FAQs, or "Dear CEO" letters.

## 4. The "Golden Dataset" (For Testing)
To evaluate the AI, we will maintain a local JSON file (`/tests/golden_dataset.json`) containing 5-10 pre-analyzed articles. 
*   **Test:** We will pass these articles through the AI processor and compare the AI's output to the human-verified "Golden" output. 
*   **Pass Criteria:** The AI must correctly classify the `status` and `jurisdiction` 100% of the time, and the `relevance_score` must be within +/- 1 point of the human score.

## 5. Hallucination Guardrails
*   **Strict Schema Enforcement:** We will use Gemini's `response_schema` parameter to force JSON output.
*   **URL Verification:** The AI must *never* generate a `source_url`. The URL must be passed into the prompt from the database and mapped back in Python.
*   **Grounding:** The prompt must explicitly state: *"If the text does not contain enough information to determine the effective date, return null. Do not guess."*
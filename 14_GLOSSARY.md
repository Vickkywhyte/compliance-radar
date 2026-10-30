# Glossary

To ensure clear communication between the developer, the AI, and future users, here are the definitions of key terms used in this project.

## Domain Terms (Compliance)
- **AML/CFT:** Anti-Money Laundering / Combating the Financing of Terrorism.
- **FATF:** Financial Action Task Force. The global watchdog that sets AML standards.
- **FIU:** Financial Intelligence Unit. The national agency that receives suspicious transaction reports (e.g., Estonian FIU).
- **FinCEN:** Financial Crimes Enforcement Network (US).
- **FCA:** Financial Conduct Authority (UK).
- **OFAC:** Office of Foreign Assets Control (US Sanctions).
- **SDN List:** Specially Designated Nationals and Blocked Persons List.

## Technical Terms (Engineering)
- **LLM:** Large Language Model (e.g., Google Gemini).
- **Pydantic:** A Python library used for data validation. Ensures the LLM outputs exactly the data types we expect.
- **RSS Feed:** A web feed format used to publish frequently updated information (used for ingestion).
- **Idempotency:** The property that a system can be run multiple times without changing the result beyond the initial application (e.g., not inserting the same article twice).
- **Cron Job:** A scheduled task (e.g., GitHub Actions running a script every day at 06:00 UTC).
- **Structured Output:** Forcing an LLM to output raw JSON that matches a specific schema, rather than conversational text.
# Global Compliance Radar (GCR) - Master Decision Document

## 1. Executive Summary
The Global Compliance Radar is designed to solve a specific enterprise problem: Information Overload in Financial Crime Compliance. We are building a zero-cost, highly scalable AI intelligence pipeline that ingests raw regulatory data (RSS/APIs), processes it using an LLM to extract structured metadata, and presents it via a filterable dashboard. 

This document outlines the strategic, architectural, and engineering decisions made during the design phase.

---

## 2. Product & Strategic Decisions

### Decision 1: B2B Utility over Personal Study Guide
* **Context:** Initially, the tool was scoped as a study guide for an interview.
* **Decision:** We pivoted the scope to a scalable B2B SaaS/intelligence platform.
* **Rationale:** Building for a broader market forces enterprise-grade design. By defining the user as a "Compliance Analyst at a Fintech," we justified the need for features like **Auditability** (source provenance), **Prioritization** (relevance scoring), and **Strict Data Contracts**. This ensures the system has real-world commercial value.

### Decision 2: "Zero-Cost MVP" Mandate
* **Context:** Building a SaaS usually incurs immediate infrastructure costs (AWS, OpenAI, Datadog).
* **Decision:** We architected the entire MVP to run on free tiers.
* **Rationale:** A senior engineer proves the *value* of a system before spending money on *scale*. We selected tools (GitHub Actions, Supabase, Gemini) that offer generous free limits. If the product gains traction, migrating to paid tiers is a configuration change, not a code rewrite.

### Decision 3: The "Global Compliance Radar" Output Format
* **Context:** Regulators publish massive, dense, unstructured text. 
* **Decision:** Instead of summarizing, the AI must output a strict "Intelligence Briefing": `Status`, `Effective Date`, `Jurisdiction`, `Relevance Score (1-10)`, and `Recommended Action`.
* **Rationale:** Compliance officers don't need another summary; they need **triage**. The Relevance Score and Recommended Action transform the tool from a "news feed" into an actionable decision-support system.

---

## 3. Architectural Decisions

### Decision 4: Modular Monolith over Microservices
* **Context:** Modern tech often defaults to microservices.
* **Decision:** We chose a Modular Monolith (a single codebase with strictly separated folders: `/ingestion`, `/ai`, `/ui`).
* **Rationale:** Microservices introduce massive operational overhead (Docker, Kubernetes, API gateways) that violates our zero-cost mandate. A modular monolith allows us to build fast now, but because the modules only communicate via the database and strict function signatures, we can extract them into microservices later without rewriting the core logic.

### Decision 5: Decoupled Ingestion and Processing
* **Context:** We could fetch an article and process it with AI in the same function.
* **Decision:** We split Data Fetching (`feeds.py`), AI Processing (`processor.py`), and DB Insertion (`database.py`) into distinct steps.
* **Rationale:** This separation of concerns ensures that if the Gemini API goes down, our system doesn't lose the ingested articles. It also makes testing much easier because we can mock the AI step while testing the ingestion step.

### Decision 6: Pydantic-First Data Contracts
* **Context:** LLMs are non-deterministic and notoriously bad at formatting data correctly.
* **Decision:** We do not trust the LLM. We defined a strict Pydantic `ComplianceEvent` model *before* writing the AI prompt.
* **Rationale:** Pydantic acts as a firewall. If the AI hallucinates a string like `"High"` instead of an integer `8` for the relevance score, Pydantic throws a `ValidationError` and prevents dirty data from entering the database. We will use Gemini's `response_schema` to force the AI to adhere to this contract.

---

## 4. Technology Stack Decisions (ADRs)

### Decision 7: PostgreSQL (via Supabase) over NoSQL (MongoDB/Firebase)
* **Context:** We needed a database with a free tier and easy Python integration.
* **Decision:** Supabase (PostgreSQL).
* **Rationale:** Compliance data is inherently relational (e.g., linking sources to jurisdictions to specific events). PostgreSQL is the industry standard for ACID-compliant relational data. Supabase provides an incredibly generous free tier, a built-in REST API, and native Row Level Security (RLS).

### Decision 8: Google Gemini Flash-Lite over OpenAI (GPT-4)
* **Context:** We needed an LLM capable of parsing long regulatory documents, outputting JSON, and costing $0.
* **Decision:** Gemini 3.1 Flash-Lite.
* **Rationale:** Gemini offers native structured JSON output (via `response_schema`) and a highly generous free API tier. The "Lite" model is specifically optimized for high-throughput extraction and avoids the 503 rate-limit errors common with the Pro/Standard models, making it perfect for a zero-cost MVP.

### Decision 9: Streamlit over React/Next.js
* **Context:** We needed a UI to display the data.
* **Decision:** Streamlit.
* **Rationale:** Since the developer is working in Python, Streamlit allows for rapid building of interactive dashboards without context-switching to HTML/CSS/JavaScript. It deploys for free on Streamlit Community Cloud. Because our architecture is decoupled, if the product scales to thousands of users, the Streamlit UI can be swapped for a React frontend without touching the backend.

### Decision 10: GitHub Actions over a Dedicated Server
* **Context:** We need to run the ingestion pipeline daily without paying for an EC2 instance.
* **Decision:** GitHub Actions (Cron Job).
* **Rationale:** GitHub Actions provides 2,000 free execution minutes per month. Our pipeline takes less than 5 minutes per day. This provides free scheduling, logging, and failure alerting out of the box.

---

## 5. Engineering Standards

### Decision 11: The "Golden Dataset" for Evaluation
* **Context:** AI pipelines can silently degrade if the model is updated or the prompt is changed.
* **Decision:** We created an Evaluation Specification with a "Golden Dataset" (human-verified articles).
* **Rationale:** Senior engineers don't just "vibe check" their AI. By maintaining a local JSON file of expected outputs, we can run automated regression tests. If the AI suddenly changes how it scores an article, the test fails, and we know our prompt needs tuning.

### Decision 12: Strict Hallucination Guardrails
* **Context:** LLMs often invent URLs or guess dates.
* **Decision:** The AI is explicitly forbidden from generating the `source_url`. The URL is passed into the prompt by Python and mapped back. The AI is instructed to return `null` for the effective date if it is not explicitly stated in the text.
* **Rationale:** In compliance, an incorrect date or a fake link is a critical failure. We enforce provenance at the system level, not the prompt level.

---

## 6. Future Scalability (Post-MVP)
While this system is built for free, the architecture is designed to scale. Future iterations will include:
1. **Multi-tenancy:** Adding Supabase Auth so different banks can have their own dashboards and custom relevance scoring.
2. **Custom Ingestion:** Allowing users to add their own RSS feeds or specific regulator URLs.
3. **Advanced Extraction:** Integrating `Unstructured.io` to parse complex PDFs and scanned documents.
4. **Webhooks:** Sending critical (Score 10) alerts directly to Slack or Microsoft Teams.

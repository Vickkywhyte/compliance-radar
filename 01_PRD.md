# Product Requirements Document (PRD)

## 1. Problem Statement
Financial institutions face an escalating volume of AML/CFT regulations, sanctions updates, and enforcement actions globally. Compliance teams manually monitor dozens of disparate sources (FATF, FinCEN, FCA, EU Commission, local FIUs). This process is inefficient, prone to human error, lacks centralized auditability, and makes it difficult to assess the *material impact* of a regulatory change on the institution.

## 2. Target Market & Personas
- **Primary Persona:** Compliance Analyst / AML Officer at a Fintech or Bank.
  - *Need:* A daily, prioritized digest of relevant regulatory changes.
- **Secondary Persona:** Chief Compliance Officer (CCO).
  - *Need:* High-level trend analysis and confidence that the institution is monitoring the right sources.

## 3. MVP Features (V1.0 - The "Zero-Cost" Proof of Concept)
- **F1 - Multi-Source Ingestion:** Pull data via RSS feeds from 5 foundational sources (e.g., FATF, FinCEN, OFAC, FCA, EU Commission).
- **F2 - AI Structuring & Scoring:** Use an LLM to parse raw text and output strict JSON containing: `Jurisdiction`, `Regulatory Status` (e.g., Proposed, In Force, Enforcement), `Effective Date`, `Relevance Score` (1-10), and a `Recommended Action`.
- **F3 - Deduplication:** Hash URLs to ensure no article is processed twice.
- **F4 - Intelligence Dashboard:** A web-based UI displaying the structured data. Must support filtering by Jurisdiction and Minimum Relevance Score.
- **F5 - Source Provenance:** Every item must display the source publication and a direct link to the original legal text.

## 4. Out of Scope (V1.0)
- Multi-tenancy / User Authentication (The MVP is a single-tenant dashboard).
- Custom user-defined source ingestion (Users cannot add their own RSS feeds yet).
- PDF extraction (V1.0 handles HTML/Text from RSS only).
- Automated report generation (e.g., exporting to PDF/Word).

## 5. Success Metrics
- **Operational:** Pipeline processes 100+ articles daily within 5 minutes, with < 1% error rate.
- **Data Quality:** AI-extracted JSON passes Pydantic schema validation 99% of the time.
- **User Value:** Reduction in time spent manually scanning regulator websites.
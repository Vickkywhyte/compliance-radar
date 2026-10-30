# Project: Global Compliance Radar (GCR)

## Mission
To build an automated, AI-driven intelligence platform that ingests global AML/CFT regulatory updates, enforcement actions, and sanctions news, transforming them into structured, actionable, and auditable compliance briefings.

## Product Vision
GCR acts as a force multiplier for compliance teams. Instead of reading hundreds of regulatory RSS feeds and news sites daily, users receive a prioritized, scored, and summarized feed of exactly what matters to their specific jurisdiction and business model.

## Current Status
- **Phase:** 1 (Foundation & Architecture)
- **Stage:** Defining PRD, Architecture, and Tech Decisions
- **Next Milestone:** Finalize Data Model & API Contracts (Phase 2)

## How to Read This Repo
1. Read `01_PRD.md` to understand the product and target market.
2. Read `02_ARCHITECTURE.md` to understand the system design and data flow.
3. Read `03_TECH_DECISIONS.md` to understand *why* we chose our stack.
4. Read `CLAUDE.md` if you are an AI assistant contributing to this codebase.
5. Read `CHANGELOG.md` for the latest engineering updates.

## Core Engineering Principles
- **Zero-Cost MVP:** Prove the value using free-tier infrastructure before scaling.
- **Idempotency:** The ingestion pipeline must be safely re-runnable without duplicating data.
- **Auditability:** Every AI-generated summary must link directly to the primary regulatory source URL. No hallucinated links.
- **Modularity:** Data ingestion, AI processing, and the UI must be decoupled. We must be able to swap the LLM (e.g., from Gemini to OpenAI) or the Database without rewriting the whole system.
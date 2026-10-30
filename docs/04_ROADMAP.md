# Project Roadmap

## Phase 1: Foundation (Current)
- [x] Create PRD
- [x] Define Architecture
- [x] Document Tech Decisions
- [ ] Define Data Model (Pydantic Schemas)
- [ ] Scaffold Repository Structure

## Phase 2: Core Engine (Backend)
- [ ] Set up Supabase Database & Tables
- [ ] Build RSS Ingestion Module
- [ ] Build AI Processor (Gemini integration)
- [ ] Build Pydantic validation for LLM outputs
- [ ] Test pipeline locally with a single RSS feed

## Phase 3: The UI (Frontend)
- [ ] Build Streamlit Dashboard
- [ ] Connect UI to Supabase
- [ ] Implement Filters (Jurisdiction, Relevance Score)

## Phase 4: Automation & Deployment
- [ ] Push repo to GitHub
- [ ] Configure GitHub Actions for daily cron job
- [ ] Deploy UI to Streamlit Community Cloud
- [ ] Run end-to-end test

## Phase 5: Future Enhancements (Post-MVP)
- [ ] Add user authentication (Supabase Auth)
- [ ] Allow users to define custom RSS feeds
- [ ] Add PDF parsing capabilities
- [ ] Implement a "Daily Email Digest" feature
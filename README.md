News Intelligence System

An AI-powered news aggregation, classification, and summarization system built as part of the **Bynd Intelligence – AI Engineering Intern Assignment**.
---

## Overview:
This project implements an end-to-end news intelligence pipeline that:
- Collects recent news articles (last 7 days)
- Classifies them by a predefined company set
- Generates concise 30–40 word summaries
- Stores structured results in a PostgreSQL database
- Exposes the data through a FastAPI backend
The system is designed with robust fallbacks, clean modular architecture, and reproducible setup.

---

## Chosen Test Set:
Global IT Companies
- Microsoft
- Google
- Apple
- Meta
Only articles related to the above companies are ingested.  
All unrelated news is filtered out.

---

## System Architecture:
News API
↓
News Fetcher (last 7 days)
↓
Deduplication (URL + hash)
↓
Entity Classification (alias-based)
↓
Content Scraping + Fallback
↓
Summarization (LLM / Offline fallback)
↓
PostgreSQL Database
↓
FastAPI Backend

---

## Tech Stack:
- Language: Python 3.10
- Database: PostgreSQL
- ORM: SQLAlchemy
- Backend: FastAPI
- News Source: NewsAPI
- Summarization:  
  - OpenAI (if you have API Key)  
  - Offline extractive fallback (for robustness)
- UI: Streamlit
- Version Control: Git & GitHub

---

## Project Structure:
 news
├── app/
│ ├── main.py # Pipeline orchestrator
│ ├── api/ # FastAPI routes
│ ├── config/ # Settings & company definitions
│ ├── db/ # Database models & CRUD
│ ├── services/ # Fetching, tagging, summarization
│ └── ui/ # Streamlit UI
├── scripts/
│ └── export_to_csv.py # CSV export utility
├── requirements.txt
├── .env.example
└── README.md

## How To Run:
Install Dependencies-
  pip install -r requirements.txt
Run the Ingestion Pipeline-
  python -m app.main
Start the API Server-
  python -m uvicorn app.api.routes:app --reload
Open API Documentation-
  http://127.0.0.1:8000/docs

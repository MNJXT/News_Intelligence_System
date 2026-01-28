# app/config/settings.py

import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# ========== Database ==========
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/bynd_news",
)

# ========== News API ==========
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_LOOKBACK_DAYS = int(os.getenv("NEWS_LOOKBACK_DAYS", 7))

# ========== LLM ==========
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SUMMARY_MIN_WORDS = 30
SUMMARY_MAX_WORDS = 40

# ========== Pipeline ==========
MAX_ARTICLES_PER_RUN = int(os.getenv("MAX_ARTICLES_PER_RUN", 100))

# ========== Logging ==========
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

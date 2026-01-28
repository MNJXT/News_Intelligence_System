# app/services/news_fetcher.py

import requests
from datetime import datetime, timedelta
from typing import List, Dict

from app.config.settings import (
    NEWS_API_KEY,
    NEWS_LOOKBACK_DAYS,
    MAX_ARTICLES_PER_RUN,
)
from app.config.companies import COMPANIES


class NewsFetcher:
    """
    Fetches recent news articles from public news APIs.
    """

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        if not NEWS_API_KEY:
            raise ValueError("NEWS_API_KEY not found in environment variables")

        self.api_key = NEWS_API_KEY

    def _build_query(self) -> str:
        """
        Builds OR-based query string from company names.
        """
        return " OR ".join(COMPANIES.keys())

    def fetch(self) -> List[Dict]:
        """
        Fetch news articles from last N days.
        Returns raw article metadata.
        """
        from_date = (
            datetime.utcnow() - timedelta(days=NEWS_LOOKBACK_DAYS)
        ).strftime("%Y-%m-%d")

        params = {
            "q": self._build_query(),
            "from": from_date,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,
            "apiKey": self.api_key,
        }

        all_articles: List[Dict] = []
        page = 1

        while len(all_articles) < MAX_ARTICLES_PER_RUN:
            params["page"] = page
            response = requests.get(self.BASE_URL, params=params, timeout=10)

            if response.status_code != 200:
                break

            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                break

            all_articles.extend(articles)

            # Stop if API has no more pages
            if len(articles) < params["pageSize"]:
                break

            page += 1

        # Cap to max allowed articles
        return all_articles[:MAX_ARTICLES_PER_RUN]

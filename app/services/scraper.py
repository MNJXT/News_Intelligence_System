# app/services/scraper.py

from typing import Optional
import trafilatura
from newspaper import Article


class ArticleScraper:
    """
    Extracts clean article text from a given URL.
    """

    @staticmethod
    def scrape(url: str) -> Optional[str]:
        """
        Attempt to scrape article content using trafilatura,
        fallback to newspaper3k if needed.
        """
        try:
            # -------- Primary: Trafilatura --------
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                extracted = trafilatura.extract(
                    downloaded,
                    include_comments=False,
                    include_tables=False,
                )
                if extracted and len(extracted.split()) > 100:
                    return extracted.strip()

            # -------- Fallback: Newspaper3k --------
            article = Article(url)
            article.download()
            article.parse()

            if article.text and len(article.text.split()) > 100:
                return article.text.strip()

        except Exception:
            # Silent failure: scraper should never break pipeline
            return None

        return None

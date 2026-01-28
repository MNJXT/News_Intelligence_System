# app/services/deduplicator.py

import hashlib
from typing import Dict
from sqlalchemy.orm import Session

from app.db.models import Article


class Deduplicator:
    """
    Handles article deduplication using URL and content hash.
    """

    @staticmethod
    def generate_content_hash(title: str, source: str) -> str:
        """
        Generate a SHA256 hash from title + source.
        Used as fallback deduplication.
        """
        raw_text = f"{title.strip().lower()}::{source.strip().lower()}"
        return hashlib.sha256(raw_text.encode("utf-8")).hexdigest()

    @staticmethod
    def is_duplicate(db: Session, article_data: Dict) -> bool:
        """
        Check if article already exists in DB.
        """
        url = article_data.get("url")
        title = article_data.get("title", "")
        source = article_data.get("source", {}).get("name", "")

        # 1. URL-based deduplication
        if db.query(Article).filter(Article.url == url).first():
            return True

        # 2. Content-hash-based deduplication
        content_hash = Deduplicator.generate_content_hash(title, source)

        if (
            db.query(Article)
            .filter(Article.content_hash == content_hash)
            .first()
        ):
            return True

        return False

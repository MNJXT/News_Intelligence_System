# scripts/export_to_csv.py

import csv
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Article, Company, article_company_map


OUTPUT_FILE = "bynd_news_output.csv"


def export_articles_to_csv():
    db: Session = SessionLocal()

    try:
        articles = db.query(Article).order_by(Article.published_at.desc()).all()

        with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                "title",
                "published_at",
                "url",
                "source",
                "companies",
                "summary",
            ])

            for article in articles:
                companies = (
                    db.query(Company)
                    .join(article_company_map)
                    .filter(article_company_map.c.article_id == article.id)
                    .all()
                )

                company_names = ", ".join([c.name for c in companies])

                writer.writerow([
                    article.title,
                    article.published_at,
                    article.url,
                    article.source,
                    company_names,
                    article.summary,
                ])

        print(f"[SUCCESS] Exported {len(articles)} articles to {OUTPUT_FILE}")

    finally:
        db.close()


if __name__ == "__main__":
    export_articles_to_csv()

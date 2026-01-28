# # app/main.py

# from sqlalchemy.orm import Session

# from app.db.session import engine, SessionLocal
# from app.db.base import Base
# from app.db import crud
# from app.db.models import Company

# from app.services.news_fetcher import NewsFetcher
# from app.services.deduplicator import Deduplicator
# from app.services.scraper import ArticleScraper
# from app.services.entity_tagger import EntityTagger
# from app.services.summarizer import ArticleSummarizer


# def init_db():
#     """
#     Create all tables.
#     """
#     Base.metadata.create_all(bind=engine)


# def run_pipeline():
#     """
#     Main orchestration logic.
#     """
#     db: Session = SessionLocal()

#     try:
#         # 1. Seed companies
#         crud.seed_companies(db)
#         companies = {c.name: c for c in crud.get_companies(db)}

#         # 2. Initialize services
#         fetcher = NewsFetcher()
#         tagger = EntityTagger()
#         summarizer = ArticleSummarizer()

#         # 3. Fetch news
#         articles = fetcher.fetch()
#         print(f"[INFO] Fetched {len(articles)} raw articles")

#         for article_data in articles:
#             # 4. Deduplication
#             if Deduplicator.is_duplicate(db, article_data):
#                 continue

#             url = article_data.get("url")
#             title = article_data.get("title")
#             description = article_data.get("description")
#             source = article_data.get("source", {}).get("name")
#             published_at = article_data.get("publishedAt")

#             # 5. Scrape article content
#             content = ArticleScraper.scrape(url)
#             if not content:
#                 continue

#             # 6. Entity tagging
#             matched_company_names = tagger.tag(
#                 title=title,
#                 description=description,
#                 content=content,
#             )

#             if not matched_company_names:
#                 continue

#             matched_companies = [
#                 companies[name] for name in matched_company_names
#                 if name in companies
#             ]

#             if not matched_companies:
#                 continue

#             # 7. Generate summary
#             summary = summarizer.summarize(content)
#             if not summary:
#                 continue

#             # 8. Content hash for dedup
#             content_hash = Deduplicator.generate_content_hash(
#                 title=title,
#                 source=source or "",
#             )

#             # 9. Persist to DB
#             crud.create_article(
#                 db=db,
#                 title=title,
#                 url=url,
#                 source=source,
#                 published_at=published_at,
#                 content=content,
#                 summary=summary,
#                 content_hash=content_hash,
#                 companies=matched_companies,
#             )

#         print("[SUCCESS] Pipeline completed successfully")

#     finally:
#         db.close()


# if __name__ == "__main__":
#     init_db()
#     run_pipeline()

# app/main.py

from sqlalchemy.orm import Session

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db import crud
from app.db.models import Company

from app.services.news_fetcher import NewsFetcher
from app.services.deduplicator import Deduplicator
from app.services.scraper import ArticleScraper
from app.services.entity_tagger import EntityTagger
from app.services.summarizer import ArticleSummarizer


def init_db():
    """
    Create all tables.
    """
    Base.metadata.create_all(bind=engine)


def run_pipeline():
    """
    Main orchestration logic.
    """
    db: Session = SessionLocal()

    try:
        # 1. Seed companies
        crud.seed_companies(db)
        companies = {c.name: c for c in crud.get_companies(db)}

        # 2. Initialize services
        fetcher = NewsFetcher()
        tagger = EntityTagger()
        summarizer = ArticleSummarizer()

        # 3. Fetch news
        articles = fetcher.fetch()
        print(f"[INFO] Fetched {len(articles)} raw articles")

        inserted = 0
        for article_data in articles:
            title = article_data.get("title")
            description = article_data.get("description")
            url = article_data.get("url")
            source = article_data.get("source", {}).get("name")
            published_at = article_data.get("publishedAt")

            if not title or not url:
                print("[SKIP] Missing title or url")
                continue

            # Deduplication
            if Deduplicator.is_duplicate(db, article_data):
                print("[SKIP] Duplicate:", title)
                continue

            # Content: scraper + fallback
            content = ArticleScraper.scrape(url)
            if not content:
                content = article_data.get("content") or description

            if not content:
                print("[SKIP] No content:", title)
                continue

            # Entity tagging
            matched_company_names = tagger.tag(
                title=title,
                description=description,
                content=content,
            )

            if not matched_company_names:
                print("[SKIP] No company match:", title)
                continue

            matched_companies = [
                companies[name]
                for name in matched_company_names
                if name in companies
            ]

            if not matched_companies:
                print("[SKIP] Company not in DB:", matched_company_names)
                continue

            # Summary (fallback-safe)
            summary = summarizer.summarize(content)

            if not summary:
                print("[SKIP] Summary failed:", title)
                continue

            # Hash
            content_hash = Deduplicator.generate_content_hash(
                title=title,
                source=source or "",
            )

            crud.create_article(
                db=db,
                title=title,
                url=url,
                source=source,
                published_at=published_at,
                content=content,
                summary=summary,
                content_hash=content_hash,
                companies=matched_companies,
            )

            print("[INSERTED]", title)

        # for article_data in articles:
        #     # 4. Deduplication
        #     if Deduplicator.is_duplicate(db, article_data):
        #         continue

        #     url = article_data.get("url")
        #     title = article_data.get("title")
        #     description = article_data.get("description")
        #     source = article_data.get("source", {}).get("name")
        #     published_at = article_data.get("publishedAt")

        #     if not title or not url:
        #         continue

        #     # 5. Try scraping full article
        #     content = ArticleScraper.scrape(url)

        #     # 🔥 FALLBACK: use NewsAPI content if scraping fails
        #     if not content:
        #         content = article_data.get("content") or description

        #     if not content:
        #         continue

        #     # 6. Entity tagging
        #     matched_company_names = tagger.tag(
        #         title=title,
        #         description=description,
        #         content=content,
        #     )

        #     # ❌ Drop articles outside chosen test set
        #     if not matched_company_names:
        #         continue

        #     matched_companies = [
        #         companies[name]
        #         for name in matched_company_names
        #         if name in companies
        #     ]

        #     if not matched_companies:
        #         continue

        #     # 7. Generate 30–40 word summary
        #     summary = summarizer.summarize(content)
        #     if not summary:
        #         continue

        #     # 8. Content hash for deduplication
        #     content_hash = Deduplicator.generate_content_hash(
        #         title=title,
        #         source=source or "",
        #     )

        #     # 9. Persist to DB
        #     crud.create_article(
        #         db=db,
        #         title=title,
        #         url=url,
        #         source=source,
        #         published_at=published_at,
        #         content=content,
        #         summary=summary,
        #         content_hash=content_hash,
        #         companies=matched_companies,
        #     )

        #     inserted += 1

        print(f"[SUCCESS] Pipeline completed successfully | Inserted {inserted} articles")

    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    run_pipeline()

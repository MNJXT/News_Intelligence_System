# app/api/routes.py

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.db.models import Article, Company, article_company_map

app = FastAPI(
    title="Bynd News Intelligence API",
    description="API for browsing AI-generated financial news summaries",
    version="1.0.0",
)


# -----------------------
# Health Check
# -----------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------
# Companies
# -----------------------

@app.get("/companies")
def list_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "aliases": c.aliases,
        }
        for c in companies
    ]


# -----------------------
# Articles
# -----------------------

@app.get("/articles")
def list_articles(
    company: Optional[str] = Query(None, description="Filter by company name"),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Article)

    if company:
        query = (
            query.join(article_company_map)
            .join(Company)
            .filter(Company.name.ilike(company))
        )

    articles = (
        query.order_by(Article.published_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": a.id,
            "title": a.title,
            "url": a.url,
            "source": a.source,
            "published_at": a.published_at,
            "summary": a.summary,
        }
        for a in articles
    ]


@app.get("/articles/{article_id}")
def get_article(article_id: UUID, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    companies = (
        db.query(Company)
        .join(article_company_map)
        .filter(article_company_map.c.article_id == article.id)
        .all()
    )

    return {
        "id": article.id,
        "title": article.title,
        "url": article.url,
        "source": article.source,
        "published_at": article.published_at,
        "content": article.content,
        "summary": article.summary,
        "companies": [c.name for c in companies],
    }

# app/db/crud.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import Article, Company
from app.config.companies import COMPANIES


# -------------------------------
# Company Operations
# -------------------------------

def seed_companies(db: Session):
    """
    Insert companies from config if they don't exist.
    Safe to run multiple times.
    """
    for name, aliases in COMPANIES.items():
        exists = db.query(Company).filter(Company.name == name).first()
        if not exists:
            company = Company(name=name, aliases=aliases)
            db.add(company)

    db.commit()


def get_companies(db: Session):
    return db.query(Company).all()


# -------------------------------
# Article Operations
# -------------------------------

def article_exists(db: Session, url: str) -> bool:
    return db.query(Article).filter(Article.url == url).first() is not None


def create_article(
    db: Session,
    title: str,
    url: str,
    source: str,
    published_at,
    content: str,
    summary: str,
    content_hash: str,
    companies: list[Company],
):
    """
    Create article and map companies.
    """
    article = Article(
        title=title,
        url=url,
        source=source,
        published_at=published_at,
        content=content,
        summary=summary,
        content_hash=content_hash,
    )

    article.companies = companies  # ORM relationship

    try:
        db.add(article)
        db.commit()
        db.refresh(article)
        return article
    except IntegrityError:
        db.rollback()
        return None

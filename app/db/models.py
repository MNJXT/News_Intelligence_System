# app/db/models.py

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Table,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from app.db.base import Base

# -------------------------------
# Association Table (Many-to-Many)
# -------------------------------

article_company_map = Table(
    "article_company_map",
    Base.metadata,
    Column("article_id", UUID(as_uuid=True), ForeignKey("articles.id"), primary_key=True),
    Column("company_id", UUID(as_uuid=True), ForeignKey("companies.id"), primary_key=True),
)

# -------------------------------
# Companies Table
# -------------------------------

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    aliases = Column(ARRAY(String), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Company(name={self.name})>"

# -------------------------------
# Articles Table
# -------------------------------

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False, unique=True)
    source = Column(String(255))
    published_at = Column(DateTime)

    content = Column(Text)
    summary = Column(Text)

    content_hash = Column(String(64), index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("url", name="uq_articles_url"),
    )

    def __repr__(self):
        return f"<Article(title={self.title[:50]})>"

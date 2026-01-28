# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # set True for SQL debugging
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependency-style DB session generator.
    Ensures session is always closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

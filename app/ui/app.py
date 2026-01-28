# app/ui/app.py

import streamlit as st
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Article, Company, article_company_map

# ----------------------------------
# Page Config
# ----------------------------------

st.set_page_config(
    page_title="Bynd News Intelligence",
    layout="wide",
)

st.title("📰 Bynd News Intelligence")
st.subheader("AI-powered summaries of financial news")

# ----------------------------------
# Database Session
# ----------------------------------

db: Session = SessionLocal()

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.header("Filters")

companies = db.query(Company).order_by(Company.name).all()
company_names = ["All"] + [c.name for c in companies]

selected_company = st.sidebar.selectbox(
    "Filter by company",
    company_names,
)

article_limit = st.sidebar.slider(
    "Number of articles",
    min_value=5,
    max_value=50,
    value=20,
)

# ----------------------------------
# Query Articles
# ----------------------------------

query = db.query(Article)

if selected_company != "All":
    query = (
        query.join(article_company_map)
        .join(Company)
        .filter(Company.name == selected_company)
    )

articles = (
    query.order_by(Article.published_at.desc())
    .limit(article_limit)
    .all()
)

# ----------------------------------
# Display Articles
# ----------------------------------

if not articles:
    st.warning("No articles found.")
else:
    for article in articles:
        with st.container():
            st.markdown(f"### {article.title}")

            meta_cols = st.columns([2, 2, 6])
            meta_cols[0].markdown(f"**Source:** {article.source}")
            meta_cols[1].markdown(
                f"**Published:** {article.published_at.strftime('%Y-%m-%d') if article.published_at else 'N/A'}"
            )
            meta_cols[2].markdown(f"[Read full article]({article.url})")

            st.markdown("**AI Summary**")
            st.write(article.summary)

            st.divider()

# ----------------------------------
# Cleanup
# ----------------------------------

db.close()

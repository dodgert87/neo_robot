from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, create_engine, MetaData, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

# Metadata object to manage table schemas
metadata = MetaData()

# Person Table
person_table = Table(
    "person", metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("first_name", String(100), nullable=True),
    Column("last_name", String(100), nullable=True),
)

# Cache Table
cache_table = Table(
    "cache", metadata,
    Column("query_id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("command", Text, nullable=False),
    Column("response", Text, nullable=False),
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False),
    Column("head_query_id", String, ForeignKey("cache.query_id"), nullable=True),
    Column("user_id", String, ForeignKey("person.id"), nullable=True),  # Make sure this matches store_query()
    Column("tag", String, nullable=False),
    Column("parameters", JSON, nullable=True),
    Column("language_code", String(2), nullable=False),
)

# News Articles Table
news_articles_table = Table(
    "news_articles", metadata,
    Column("article_id", String, primary_key=True, unique=True, nullable=False),  # Unique article ID from API
    Column("query_id", String, ForeignKey("cache.query_id"), nullable=True),  # Links to queries in cache
    Column("title", Text, nullable=False),  # Article title
    Column("keywords", JSON, nullable=True),  # List of keywords for searching
    Column("creator", JSON, nullable=True),  # List of authors
    Column("description", Text, nullable=True),  # Short description
    Column("content", Text, nullable=True),  # Full content (if available)
    Column("pub_date", DateTime, nullable=False),  # Publication date
    Column("language", String(50), nullable=False),  # Language of the article
    Column("category", JSON, nullable=True),  # List of categories (e.g., sports, business)
    Column("country", JSON, nullable=True),  # List of relevant countries
    Column("source_id", String, nullable=True),  # Source identifier (e.g., BBC, Reuters)
    Column("source_name", String, nullable=True),  # Name of the source (e.g., BBC News)
    Column("source_url", String, nullable=True),  # Source website URL
    Column("image_url", String, nullable=True),  # URL of the article's image
    Column("query_count", Integer, default=0, nullable=False),  # Tracks how many times this article is queried
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False),  # When it was stored in DB
)

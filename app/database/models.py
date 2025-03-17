from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON, create_engine, MetaData, Table
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
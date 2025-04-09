from sqlalchemy import Column, Float, Integer, String, Text, ForeignKey, DateTime, JSON, MetaData, Table
from datetime import datetime, timezone
import uuid

from app.core.enums import UserType

# Metadata object to manage table schemas
metadata = MetaData()

# -------------------- Person Table --------------------
person_table = Table(
    "person", metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("first_name", String(100), nullable=True),
    Column("last_name", String(100), nullable=True),
)

# -------------------- Command Table --------------------
command_table = Table(
    "command", metadata,
    Column("command_id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("chat_id", String, nullable=False),  # To relate the command to its session
    Column("tag", String, nullable=False),  # Enum: weather, news, joke, etc.
    Column("raw_command", Text, nullable=False),  # Original natural language input from the user
    Column("parsed_command", JSON, nullable=False),  # JSON: {"command": "...", "parameters": {...}}
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

# -------------------- Unknown Person Table --------------------
unknown_person_table = Table(
    "unknown_person", metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("session_token", String(100), nullable=False, unique=True),  # Could be a random hash or session ID
    Column("created_at", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

# -------------------- Cache Table (Master) --------------------
cache_table = Table(
    "cache", metadata,
    Column("chat_id", String, primary_key=True, unique=True, nullable=False),  # No default; generated manually
    Column("user_id", String, ForeignKey("person.id"), nullable=True),
    Column("user_type", String, nullable=False, default=UserType.UNKNOWN.value),  # KNOWN or UNKNOWN
    Column("language_code", String(2), nullable=False),
    Column("history", JSON, nullable=False),  # Format: [{"command_id": "...", "response_id": "..."}, ...]
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

# -------------------- News Articles Table --------------------
news_articles_table = Table(
    "news_articles", metadata,
    Column("article_id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("query_id", String, ForeignKey("cache.chat_id"), nullable=True),
    Column("title", Text, nullable=False),
    Column("keywords", JSON, nullable=True),
    Column("creator", JSON, nullable=True),
    Column("description", Text, nullable=True),
    Column("content", Text, nullable=True),
    Column("pub_date", DateTime, nullable=False),
    Column("language", String(50), nullable=False),
    Column("category", JSON, nullable=True),
    Column("country", JSON, nullable=True),
    Column("source_id", String, nullable=True),
    Column("source_name", String, nullable=True),
    Column("source_url", String, nullable=True),
    Column("image_url", String, nullable=True),
    Column("query_count", Integer, default=0, nullable=False),
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

# -------------------- Weather Data Table --------------------
weather_data_table = Table(
    "weather_data", metadata,
    Column("weather_id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("query_id", String, ForeignKey("cache.chat_id"), nullable=True),
    Column("location", String(100), nullable=False),
    Column("region", String(100), nullable=True),
    Column("country", String(100), nullable=True),
    Column("last_updated", DateTime, nullable=False),
    Column("temperature_c", Float, nullable=True),
    Column("condition", String(100), nullable=True),
    Column("humidity", Integer, nullable=True),
    Column("wind_speed_kph", Float, nullable=True),
    Column("feels_like_c", Float, nullable=True),
    Column("cloud_cover", Integer, nullable=True),
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

# -------------------- General Knowledge Table --------------------
general_table = Table(
    "general_data", metadata,
    Column("general_id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("query_id", String, ForeignKey("cache.chat_id"), nullable=True),
    Column("content", Text, nullable=False),
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

# -------------------- Joke Table --------------------
joke_table = Table(
    "joke_data", metadata,
    Column("joke_id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("query_id", String, ForeignKey("cache.chat_id"), nullable=True),
    Column("content", Text, nullable=False),
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

# -------------------- Story Table --------------------
story_table = Table(
    "story_data", metadata,
    Column("story_id", String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False),
    Column("query_id", String, ForeignKey("cache.chat_id"), nullable=True),
    Column("content", Text, nullable=False),
    Column("timestamp", DateTime, default=datetime.now(timezone.utc), nullable=False)
)

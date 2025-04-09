from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import Engine
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.database.models import (
    person_table, unknown_person_table, cache_table,
    news_articles_table, weather_data_table,
    general_table, joke_table, story_table,
    command_table
)

class DatabaseService:
    def __init__(self, engine: Engine):
        self.engine = engine

    # -------------------- Person Table --------------------
    def create_person(self, data: Dict[str, Any]) -> str:
        with self.engine.begin() as conn:
            result = conn.execute(insert(person_table).values(**data))
            return result.inserted_primary_key[0]

    def get_person(self, person_id: str) -> Optional[Dict[str, Any]]:
        with self.engine.begin() as conn:
            result = conn.execute(select(person_table).where(person_table.c.id == person_id)).fetchone()
            return dict(result) if result else None

    def update_person(self, person_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(person_table).where(person_table.c.id == person_id).values(**updates))

    def delete_person(self, person_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(person_table).where(person_table.c.id == person_id))

    # -------------------- Cache Table --------------------
    def create_cache_record(self, user_id: str, user_type: str, language_code: str) -> str:
        chat_id = f"{user_id}_{datetime.timezone.utc.strftime('%Y-%m-%d')}"
        with self.engine.begin() as conn:
            conn.execute(
                insert(cache_table).values(
                    chat_id=chat_id,
                    user_id=user_id,
                    user_type=user_type,
                    language_code=language_code,
                    history=[],
                    timestamp=datetime.now(datetime.timezone.utc)
                )
            )
            return chat_id

    def append_to_history(self, chat_id: str, command_id: str, response_id: str) -> None:
        with self.engine.begin() as conn:
            result = conn.execute(select(cache_table.c.history).where(cache_table.c.chat_id == chat_id)).fetchone()
            if not result:
                raise ValueError(f"Cache record not found for chat_id={chat_id}")
            history = result.history or []
            history.append({"command_id": command_id, "response_id": response_id})
            conn.execute(
                update(cache_table).where(cache_table.c.chat_id == chat_id).values(history=history)
            )

    def get_history(self, chat_id: str) -> List[Dict[str, str]]:
        with self.engine.begin() as conn:
            result = conn.execute(select(cache_table.c.history).where(cache_table.c.chat_id == chat_id)).fetchone()
            return result.history if result else []

    def update_cache_record(self, chat_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(cache_table).where(cache_table.c.chat_id == chat_id).values(**updates))

    def delete_cache_record(self, chat_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(cache_table).where(cache_table.c.chat_id == chat_id))

    # -------------------- Command Table --------------------
    def save_command(self, chat_id: str, tag: str, raw: str, parsed: Dict[str, Any]) -> str:
        with self.engine.begin() as conn:
            result = conn.execute(
                insert(command_table).values(
                    chat_id=chat_id,
                    tag=tag,
                    raw_command=raw,
                    parsed_command=parsed,
                    timestamp=datetime.now(datetime.timezone.utc)
                )
            )
            return result.inserted_primary_key[0]

    def get_command(self, command_id: str) -> Optional[Dict[str, Any]]:
        with self.engine.begin() as conn:
            result = conn.execute(select(command_table).where(command_table.c.command_id == command_id)).fetchone()
            return dict(result) if result else None

    def update_command(self, command_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(command_table).where(command_table.c.command_id == command_id).values(**updates))

    def delete_command(self, command_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(command_table).where(command_table.c.command_id == command_id))

    # -------------------- News Articles --------------------
    def create_news_article(self, data: Dict[str, Any]) -> str:
        with self.engine.begin() as conn:
            result = conn.execute(insert(news_articles_table).values(**data))
            return result.inserted_primary_key[0]

    def get_news_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        with self.engine.begin() as conn:
            row = conn.execute(select(news_articles_table).where(news_articles_table.c.article_id == article_id)).fetchone()
            return dict(row) if row else None

    def update_news_article(self, article_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(news_articles_table).where(news_articles_table.c.article_id == article_id).values(**updates))

    def delete_news_article(self, article_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(news_articles_table).where(news_articles_table.c.article_id == article_id))

    # -------------------- Weather Data --------------------
    def create_weather_data(self, data: Dict[str, Any]) -> str:
        with self.engine.begin() as conn:
            result = conn.execute(insert(weather_data_table).values(**data))
            return result.inserted_primary_key[0]

    def get_weather_data(self, weather_id: str) -> Optional[Dict[str, Any]]:
        with self.engine.begin() as conn:
            row = conn.execute(select(weather_data_table).where(weather_data_table.c.weather_id == weather_id)).fetchone()
            return dict(row) if row else None

    def update_weather_data(self, weather_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(weather_data_table).where(weather_data_table.c.weather_id == weather_id).values(**updates))

    def delete_weather_data(self, weather_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(weather_data_table).where(weather_data_table.c.weather_id == weather_id))

    # -------------------- General Data --------------------
    def create_general_data(self, data: Dict[str, Any]) -> str:
        with self.engine.begin() as conn:
            result = conn.execute(insert(general_table).values(**data))
            return result.inserted_primary_key[0]

    def get_general_data(self, general_id: str) -> Optional[Dict[str, Any]]:
        with self.engine.begin() as conn:
            row = conn.execute(select(general_table).where(general_table.c.general_id == general_id)).fetchone()
            return dict(row) if row else None

    def update_general_data(self, general_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(general_table).where(general_table.c.general_id == general_id).values(**updates))

    def delete_general_data(self, general_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(general_table).where(general_table.c.general_id == general_id))

    # -------------------- Joke Data --------------------
    def create_joke(self, data: Dict[str, Any]) -> str:
        with self.engine.begin() as conn:
            result = conn.execute(insert(joke_table).values(**data))
            return result.inserted_primary_key[0]

    def get_joke(self, joke_id: str) -> Optional[Dict[str, Any]]:
        with self.engine.begin() as conn:
            row = conn.execute(select(joke_table).where(joke_table.c.joke_id == joke_id)).fetchone()
            return dict(row) if row else None

    def update_joke(self, joke_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(joke_table).where(joke_table.c.joke_id == joke_id).values(**updates))

    def delete_joke(self, joke_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(joke_table).where(joke_table.c.joke_id == joke_id))

    # -------------------- Story Data --------------------
    def create_story(self, data: Dict[str, Any]) -> str:
        with self.engine.begin() as conn:
            result = conn.execute(insert(story_table).values(**data))
            return result.inserted_primary_key[0]

    def get_story(self, story_id: str) -> Optional[Dict[str, Any]]:
        with self.engine.begin() as conn:
            row = conn.execute(select(story_table).where(story_table.c.story_id == story_id)).fetchone()
            return dict(row) if row else None

    def update_story(self, story_id: str, updates: Dict[str, Any]) -> None:
        with self.engine.begin() as conn:
            conn.execute(update(story_table).where(story_table.c.story_id == story_id).values(**updates))

    def delete_story(self, story_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(delete(story_table).where(story_table.c.story_id == story_id))

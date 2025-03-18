import json
import sqlite3
from datetime import datetime, timezone
from app.core.error_codes import ErrorCode
from app.core.config import settings

class CacheService:
    """
    Handles caching of queries and users in the database.
    """

    DB_PATH = settings.DATABASE_URL.replace("sqlite:///", "")

    @staticmethod
    def _connect():
        """Establishes a connection to the SQLite database."""
        return sqlite3.connect(CacheService.DB_PATH)

    @staticmethod
    def store_query(query_id: str, user_id: str, command: str, tag: str, parameters: dict, response: str, language_code: str, head_query_id: str = None):
        """
        Stores a query response in the database.
        """
        print (command)
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO cache (query_id, command, tag, parameters, response, timestamp, language_code, user_id, head_query_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (query_id, command, tag, json.dumps(parameters), response, datetime.now(timezone.utc), language_code, user_id, head_query_id))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error storing query: {e}")

    @staticmethod
    def retrieve_query(query_id=None, command=None, tag=None, parameters=None, user_id=None, head_query_id=None):
        """
        Retrieves a cached query from the database.
        Allows filtering by query_id, command, tag, parameters, user_id, or head_query_id.
        """
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            # Construct base query
            query = """
                SELECT query_id, command, response, timestamp, tag, parameters, language_code, user_id, head_query_id
                FROM cache
                WHERE 1=1
            """
            values = []

            # Apply filters
            if query_id:
                query += " AND query_id = ?"
                values.append(query_id)
            if command:
                query += " AND command = ?"
                values.append(command)
            if tag:
                query += " AND tag = ?"
                values.append(tag)
            if parameters:
                query += " AND parameters LIKE ?"
                values.append(f"%{json.dumps(parameters)}%")
            if user_id:
                query += " AND user_id = ?"
                values.append(user_id)
            if head_query_id:
                query += " AND head_query_id = ?"
                values.append(head_query_id)

            # Execute query
            cursor.execute(query, values)
            result = cursor.fetchall()
            conn.close()

            # Convert result to dictionary format
            queries = []
            for row in result:
                queries.append({
                    "queryId": row[0],
                    "command": row[1],
                    "response": row[2],
                    "timestamp": row[3],
                    "tag": row[4],
                    "parameters": json.loads(row[5]) if row[5] else {},
                    "language_code": row[6],
                    "user_id": row[7],
                    "head_query_id": row[8],
                })

            return queries

        except Exception as e:
                print(f"Error retrieving query: {e}")
                return {"error": "Database retrieval error", "error_code": ErrorCode.INTERNAL_ERROR.value}


    @staticmethod
    def store_person(person_id: str, first_name: str, last_name: str):
        """
        Stores a person's information.
        """
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO person (id, first_name, last_name)
                VALUES (?, ?, ?)
            """, (person_id, first_name, last_name))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error storing person: {e}")

    @staticmethod
    def retrieve_person(person_id: str):
        """
        Retrieves a person from the database using their ID.
        """
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, first_name, last_name FROM person WHERE id = ?
            """, (person_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return {"id": row[0], "first_name": row[1], "last_name": row[2]}
            else:
                return {"error": "Person not found", "error_code": ErrorCode.INTERNAL_ERROR.value}

        except Exception as e:
            print(f"Error retrieving person: {e}")
            return {"error": "Database retrieval error", "error_code": ErrorCode.INTERNAL_ERROR.value}

    @staticmethod
    def retrieve_all_persons():
        """
        Retrieves all persons stored in the database.
        """
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, first_name, last_name FROM person
            """)

            rows = cursor.fetchall()
            conn.close()

            persons = [
                {"id": row[0], "first_name": row[1], "last_name": row[2]}
                for row in rows
            ]

            return persons

        except Exception as e:
            print(f"Error retrieving persons: {e}")
            return {"error": "Database retrieval error", "error_code": ErrorCode.INTERNAL_ERROR.value}


    @staticmethod
    def store_news_article(article_data: dict):
        """
        Stores a news article in the database, avoiding duplicates.
        """
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            # Check if the article already exists
            cursor.execute("SELECT article_id FROM news_articles WHERE article_id = ?", (article_data["article_id"],))
            existing = cursor.fetchone()

            if existing:
                print(f"Article {article_data['article_id']} already exists. Skipping insert.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO news_articles (
                    article_id, query_id, title, keywords, creator, description, content,
                    pub_date, language, category, country, source_id, source_name,
                    source_url, image_url, query_count, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article_data["article_id"],
                article_data.get("query_id"),
                article_data["title"],
                json.dumps(article_data.get("keywords", [])),
                json.dumps(article_data.get("creator", [])),
                article_data.get("description"),
                article_data.get("content"),
                article_data["pubDate"],
                article_data["language"],
                json.dumps(article_data.get("category", [])),
                json.dumps(article_data.get("country", [])),
                article_data.get("source_id"),
                article_data.get("source_name"),
                article_data.get("source_url"),
                article_data.get("image_url"),
                0,  # Initial query count is 0
                datetime.now(timezone.utc)
            ))

            conn.commit()
            conn.close()
            print(f"Stored article {article_data['article_id']} successfully.")

        except Exception as e:
            print(f"Error storing news article: {e}")

    @staticmethod
    def fetch_articles(article_id=None, title=None, keywords=None, category=None, country=None, source_id=None):
        """
        Fetches news articles dynamically based on provided filters.
        If an article is found, it automatically increments the query count.
        """
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            query = "SELECT * FROM news_articles WHERE 1=1"
            values = []

            if article_id:
                query += " AND article_id = ?"
                values.append(article_id)
            if title:
                query += " AND title LIKE ?"
                values.append(f"%{title}%")
            if keywords:
                query += " AND keywords LIKE ?"
                values.append(f"%{json.dumps(keywords)}%")
            if category:
                query += " AND category LIKE ?"
                values.append(f"%{json.dumps(category)}%")
            if country:
                query += " AND country LIKE ?"
                values.append(f"%{json.dumps(country)}%")
            if source_id:
                query += " AND source_id = ?"
                values.append(source_id)

            cursor.execute(query, values)
            result = cursor.fetchall()

            articles = []
            for row in result:
                article_id = row[0]  # Extract article_id
                articles.append({
                    "article_id": article_id,
                    "query_id": row[1],
                    "title": row[2],
                    "keywords": json.loads(row[3]) if row[3] else [],
                    "creator": json.loads(row[4]) if row[4] else [],
                    "description": row[5],
                    "content": row[6],
                    "pubDate": row[7],
                    "language": row[8],
                    "category": json.loads(row[9]) if row[9] else [],
                    "country": json.loads(row[10]) if row[10] else [],
                    "source_id": row[11],
                    "source_name": row[12],
                    "source_url": row[13],
                    "image_url": row[14],
                    "query_count": row[15],
                    "timestamp": row[16]
                })

                # **Auto-Increment Query Count for Retrieved Articles**
                CacheService.increment_query_count(article_id)

            conn.close()
            return articles

        except Exception as e:
            print(f"Error retrieving news articles: {e}")
            return {"error": "Database retrieval error", "error_code": ErrorCode.INTERNAL_ERROR.value}



    @staticmethod
    def increment_query_count(article_id: str):
        """
        Increments the query count for a news article.
        """
        try:
            conn = CacheService._connect()
            cursor = conn.cursor()

            cursor.execute("UPDATE news_articles SET query_count = query_count + 1 WHERE article_id = ?", (article_id,))
            conn.commit()
            conn.close()

            print(f"Incremented query count for article {article_id}.")

        except Exception as e:
            print(f"Error updating query count: {e}")

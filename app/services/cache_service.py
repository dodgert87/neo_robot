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
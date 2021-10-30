import os
import psycopg2
from psycopg2.extras import DictCursor


def init():
    _create_tables()


def _get_connection():
    try:
        return psycopg2.connect(os.environ["DATABASE_URL"])
    except Exception as e:
        raise


def _create_tables():
    try:
        with _get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE messages (\
                        id SERIAL NOT NULL,\
                        body TEXT NOT NULL,\
                        created_at TIMESTAMP DEFAULT NOW(),\
                        updated_at TIMESTAMP DEFAULT NOW(),\
                        PRIMARY KEY (id)\
                    );"
                )
            conn.commit()
    except psycopg2.errors.DuplicateTable as e:
        print(e)
    except Exception as e:
        raise


def get_message_by_random():
    try:
        with _get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    "SELECT body FROM messages ORDER BY RANDOM() limit 1",
                )

                return cur.fetchone()
    except Exception as e:
        raise


def _add_message(body):
    try:
        with _get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO messages (body) VALUES (%s)",
                    (body,),
                )
            conn.commit()
    except Exception as e:
        raise


def _delete_all_messages():
    try:
        with _get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM messages",
                )
            conn.commit()
    except Exception as e:
        raise

import sqlite3
from contextlib import contextmanager

import pandas as pd

from settings import DB_NAME


def fetch_data(table_name="book_info"):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


@contextmanager
def db_transaction():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e


def get_table_names():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]


def create_tables():
    with db_transaction() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                author_id INTEGER,
                num_pages INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        """)


def add_book(name, author, num_pages):
    with db_transaction() as cursor:
        cursor.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author,))
        cursor.execute("SELECT id FROM authors WHERE name = ?", (author,))
        author_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO books (name, author_id, num_pages) VALUES (?, ?, ?)",
                       (name, author_id, num_pages))

        book_table_name = name.replace(" ", "_").lower()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {book_table_name} (
                page_start TIMESTAMP,
                page_end TIMESTAMP,
                page_number INTEGER
            )
        """)


def log_reading_session(book_name, page_number, page_start, page_end):
    with db_transaction() as cursor:
        book_table_name = book_name.replace(" ", "_").lower()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {book_table_name} (
                page_start TIMESTAMP,
                page_end TIMESTAMP,
                page_number INTEGER
            )
        """)
        cursor.execute(f"""
            INSERT INTO {book_table_name} (page_start, page_end, page_number)
            VALUES (?, ?, ?)
        """, (page_number, page_start, page_end))


def get_book_name_from_id(book_id):
    with db_transaction() as cursor:
        cursor.execute("SELECT Title FROM book_info WHERE rowid = ?", (book_id,))
        return cursor.fetchone()[0]

# create_tables()
# add_book("Example Book", "John Doe", 300)
# log_reading_session("Example_Book", "2023-01-01 10:00:00", "2023-01-01 10:30:00", 5)

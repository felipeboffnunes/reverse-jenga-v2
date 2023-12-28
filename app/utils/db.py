import sqlite3
from contextlib import contextmanager

import pandas as pd

from settings import DB_NAME, DB_REVJ1


def fetch_data(table_name="book_info"):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


@contextmanager
def db_transaction(db_name=DB_NAME):
    print(db_name)
    with sqlite3.connect(db_name) as conn:
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

    # select book name from book id of options inside sessions table with book_id as reference
    # Select all book_ids unique
    cursor.execute("SELECT DISTINCT book_id FROM sessions")
    book_ids = cursor.fetchall()
    book_ids = [book_id[0] for book_id in book_ids]
    placeholders = ', '.join('?' for _ in book_ids)

    cursor.execute("SELECT Title FROM book_info WHERE rowid IN ({})".format(placeholders), tuple(book_ids))

    book_names = cursor.fetchall()
    book_names = [table[0] for table in book_names]
    book_names.append("All Books")
    book_ids.append("all")
    combined = list(zip(book_names, book_ids))

    conn.close()
    return combined


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


def log_reading_session(book_id, page_start, page_end):



    with db_transaction(DB_REVJ1) as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS sessions (
                book_id INTEGER,
                page_start DATE,
                page_end DATE
            )
        """)
        cursor.execute(f"""
            INSERT INTO sessions (book_id, page_start, page_end)
            VALUES (?, ?, ?)
        """, (book_id, page_start, page_end))


def get_book_name_from_id(book_id):
    with db_transaction(DB_REVJ1) as cursor:
        cursor.execute("SELECT Title FROM book_info WHERE rowid = ?", (book_id,))
        return cursor.fetchone()[0]

# create_tables()
# add_book("Example Book", "John Doe", 300)
# log_reading_session("Example_Book", "2023-01-01 10:00:00", "2023-01-01 10:30:00", 5)


def add_book(title, author, pages):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO book_info (Title, Author, Pages) VALUES (?, ?, ?)",
                   (title, author, pages))
    conn.commit()
    conn.close()


def get_session_data(book_id:int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM sessions WHERE book_id == {book_id}")
    session_data = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(session_data, columns=['book_id', 'page_start', 'page_end'])
    print(df.head())
    return df

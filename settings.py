from datetime import timedelta

DB_NAME = "./reverse-jenga-v1/books_database.db"
DB_REVJ1 = "./books_database.db"
SESSION_DELTA = timedelta(hours=2)
PARAMS = {
    'OVERLOAD_TASK_SIZE': 10,
    'PAGE_GOAL': 0,
    'BOOK_ID': 0,
}

PATHS = {
    'ASCII_DIR': "./assets/ascii/",
    'DATA_DIR': "./data/",
}

CONFIG = {
    'CONSOLE': {
        'COLS': '105',
        'LINES': '37',
    }
}
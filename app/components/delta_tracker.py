import sqlite3
from datetime import timedelta

import pandas as pd

from settings import DB_NAME


def process_session_data(book_id: int):
    conn = sqlite3.connect(DB_NAME)
    if book_id == "all":
        df = pd.read_sql_query("SELECT * FROM sessions", conn)
    else:
        df = pd.read_sql_query(f"SELECT * FROM sessions WHERE book_id == {book_id}", conn)
    conn.close()
    if df.empty:
        return df, 0, 0, 0, 0
    # Convert timestamps to datetime

    df['page_start'] = pd.to_datetime(df['page_start'])
    df['page_end'] = pd.to_datetime(df['page_end'])
    # Calculate metrics
    df['read_time'] = (df['page_end'] - df['page_start']).dt.total_seconds() / 60
    # print number of read_time values that are less than 0
    print(df['read_time'])
    window_size = "T"
    df['moving_avg'] = df['read_time'].rolling(5).mean()
    df['date'] = df['page_start'].dt.date
    return df


# Calculate the moving average



# Plot using Plotly Express

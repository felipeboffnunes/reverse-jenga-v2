from timeit import default_timer

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from data_handler import DataHandler



def generate_fake_reading_data(num_pages, avg_time_per_page, variability, session_break_chance=0.05):
    """
    Generate fake reading session data.

    :param num_pages: Number of pages in the book.
    :param avg_time_per_page: Average time taken to read a page in minutes.
    :param variability: Variability in time per page to simulate distractions (in minutes).
    :param start_date: The start date of the reading.
    :param session_break_chance: Chance to start a new reading session.
    :return: DataFrame with fake reading session data.
    """
    data = {'_page_start': [], '_page_end': []}
    current_time = datetime.now()
    last_current_time = current_time
    book_id = 1
    for i in range(num_pages):
        # using i, change the book_id after a certain amount of pages incrementally
        if i % 200 == 0:
            book_id += 1

        # add three to seven minutes to the current time, as page_end
        page_end = last_current_time + timedelta(minutes=random.randint(0, 3))
        data['_page_start'].append(last_current_time)
        last_current_time = page_end
        data['_page_end'].append(page_end)

        DataHandler.save_page(book_id, pd.DataFrame(data))

    return pd.DataFrame(data)

num_pages = 600  # Total number of pages in the book
avg_time_per_page = 8  # Average time to read a page in
variability = 3  # Variability in time per page to simulate distractions
generate_fake_reading_data(num_pages, avg_time_per_page, variability)
# Generate fake data

import pandas as pd

from app.utils.db import log_reading_session, get_book_name_from_id


class DataHandler:

    @staticmethod
    def save_page(book_id: int, tracker_data: pd.DataFrame) -> None:
        data_from_tracker = tracker_data.tail(1)
        #page_number = data_from_tracker['page_number'].values[0]
        page_start = data_from_tracker['_page_start'].values[0]
        page_end = data_from_tracker['_page_end'].values[0]
        #print(f"Saving page {page_number} from {book_id}...")
        print(f"Page start: {page_start}")
        print(f"Page end: {page_end}")
        # transform numpy.datetimes into sqlites friendly format
        page_start = page_start.astype('datetime64[s]').astype('str')
        page_end = page_end.astype('datetime64[s]').astype('str')

        log_reading_session(book_id, page_start, page_end)

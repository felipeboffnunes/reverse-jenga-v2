
from dataclasses import dataclass, field
from datetime import datetime
from timeit import default_timer

import pandas as pd


def get_tracker_dataframe() -> pd.DataFrame:
    return pd.DataFrame({
        'page_number': pd.Series(dtype='int64'),
        'page_start': pd.Series(dtype='timedelta64[s]'),
        'page_end': pd.Series(dtype='timedelta64[s]')
    })


@dataclass
class Tracker:

    first_frame: float = field(init=False)
    current_frame: float = field(init=False)

    page_count: int = 0
    data: pd.DataFrame = field(init=False, default_factory=get_tracker_dataframe, repr=False)

    def start(self) -> None:
        self.first_frame = self.current_frame = default_timer()
        self.first_date = self.current_date = datetime.now()

    def update(self) -> None:
        frame = default_timer()
        date = datetime.now()

        data_row = pd.DataFrame([{
            'page_number': self.page_count,
            'page_start': self.current_frame,
            'page_end': frame,
            '_page_start': self.current_date,
            '_page_end': date
        }])

        self.page_count += 1
        self.current_frame = frame
        self.current_date = date
        self.data = pd.concat([self.data, data_row], ignore_index=True)

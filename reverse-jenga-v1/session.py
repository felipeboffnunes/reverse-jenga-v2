
from dataclasses import dataclass, field

from numpy import ndarray

from settings import PARAMS
from data_handler import DataHandler
from tracker import Tracker


@dataclass
class Session:

    book_id: int = field(init=False, default=PARAMS['BOOK_ID'])
    page_goal: int = field(init=False, default=PARAMS['PAGE_GOAL'])
    complete: bool = field(init=False, default=False)
    overload: bool = field(init=False, default=False)

    _tracker: Tracker = field(init=False, default_factory=Tracker, repr=False)

    def __post_init__(self) -> None:
        self._tracker.start()

    def update(self) -> None:
        self._tracker.update()
        DataHandler.save_page(self.book_id, self._tracker.data)
        if self._tracker.page_count == self.page_goal:
            self.complete = True

    def get_tracker_tail_array(self, rows: int = 25) -> ndarray:
        return self._tracker.data.tail(n=rows).to_numpy()[::-1]

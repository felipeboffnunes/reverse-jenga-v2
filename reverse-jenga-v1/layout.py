
from dataclasses import dataclass, field
from functools import cached_property

from numpy import ndarray
from rich.console import Console
from rich.layout import Layout
from rich.progress import Progress, TaskID
from rich.table import Column, Table

from settings import PARAMS
from load_ascci import load_ascii


@dataclass
class LayoutHandler:

    layout: Layout = field(init=False)
    progress: Progress = field(init=False)
    console: Console = field(init=False, default_factory=Console)
    table: Table = field(init=False)

    def __post_init__(self) -> None:
        self.setup_layout()

    def set_table_layout(self) -> None:
        self.table = Table(
            Column('Time', justify='left'),
            Column('Page', justify='center'),
            Column('Time Frame', justify='right')
        )

    def refresh_table(self, tracker_tail_array: ndarray) -> None:
        self.set_table_layout()
        for page_number, page_start, page_end, _, _ in tracker_tail_array:
            delta = page_end - page_start
            self.table.add_row(
                str(page_start)[:-4],
                str(page_number),
                str(delta)[:-4]
            )

    def set_progress_layout(self) -> None:
        self.progress = Progress()
        self.progress.add_task("[green]Progress...", total=PARAMS['PAGE_GOAL'])

    def add_progress_task(self) -> None:
        self.progress.add_task("[red]Overload...", total=PARAMS['OVERLOAD_TASK_SIZE'])

    def update_progress(self, overload: bool = False) -> None:
        self.progress.update(TaskID(1 if overload else 0), advance=1)

    def refresh_output(self, tracker_tail_array: ndarray, overload: bool) -> None:
        self.refresh_table(tracker_tail_array)
        self.update_layout()
        self.update_progress(overload)
        self.refresh_console()

    def setup_layout(self) -> None:
        self.set_progress_layout()
        self.set_table_layout()

        self.layout = Layout()
        self.layout.split_column(
            Layout('\n', name='padding_top'),
            Layout(name='main', ratio=12)
        )
        self.layout['main'].split_row(
            Layout(self.table, name='tracker', ratio=3),
            Layout(name='right', ratio=6),

        )
        self.layout['right'].split_column(
            Layout(self.ascii_taico, name='ascii', ratio=10),
            Layout(self.progress, name='progress', ratio=2),
        )

    def update_layout(self) -> None:
        self.layout['tracker'].update(self.table)

    def refresh_console(self) -> None:
        self.console.clear()
        self.console.print(self.layout)

    def session_started(self) -> None:
        self.console.clear()
        self.console.print(
            "[green]Session initialized![/green]\n"
            "[bold]Press Enter when you have finished reading the first page[/bold]"
        )

    @cached_property
    def ascii_taico(self) -> str:
        return load_ascii('taico.txt')

    @cached_property
    def ascii_arson(self) -> str:
        return load_ascii('arson.txt')

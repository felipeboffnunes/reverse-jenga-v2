from dataclasses import dataclass, field

from rich.prompt import Confirm, Prompt

from layout import LayoutHandler
from session import Session


@dataclass
class Chrono:
    session: Session = field(init=False, default_factory=Session)
    layout: LayoutHandler = field(init=False, default_factory=LayoutHandler)

    def __post_init__(self):
        self.start()

    def start(self):
        self.layout.session_started()
        self.handle_session()

    def handle_session(self):
        while self.ask_next_step():
            self.session.update()

            data = self.session.get_tracker_tail_array()
            self.layout.refresh_output(data, self.session.overload)

            # TODO: overload is deprecated
            if self.session.complete and not self.session.overload:
                if self.ask_overload_start():
                    self.session.overload = True
                    self.layout.add_progress_task()
                else:
                    break
            elif self.layout.progress.finished:
                break

        self.finish_session()

    @staticmethod
    def ask_next_step() -> bool:
        return Confirm.ask(
            "Press [Enter] to continue / Quit [0]",
            choices=['', '0'],
            show_choices=False
        )

    @staticmethod
    def ask_overload_start() -> bool:
        return Confirm.ask(
            "You have reached your page goal for this session.\n"
            "Do you want to continue on overload?"
        )

    def finish_session(self) -> None:
        self.layout.console.print("[green]Session saved!")
        if self.session.complete:
            print("Good bye, Tony Hawk.")
        else:
            print("Well, you have tried. Right? Forget it... Go.")

    @staticmethod
    def dialogue_begin() -> None:
        Prompt.ask(
            "Did you get some coffee?\n"
            "Prepare yourself, do not get distracted.\n"
            "Press [Enter] to begin"
        )

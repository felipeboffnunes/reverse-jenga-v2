
import os

from rich.prompt import IntPrompt

from settings import PARAMS, CONFIG
from load_ascci import load_ascii


def setup_parameters() -> None:
    setup_console_size()
    print(load_ascii('arson.txt'))
    PARAMS['PAGE_GOAL'] = IntPrompt.ask("Page goal")
    PARAMS['BOOK_ID'] = IntPrompt.ask("Book id")


def setup_console_size() -> None:
    os.system(f"mode con: cols={CONFIG['CONSOLE']['COLS']} lines={CONFIG['CONSOLE']['LINES']}")

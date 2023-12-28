
from pathlib import Path

from settings import PATHS


def load_ascii(ascii_asset: str) -> str:
    path = Path(PATHS['ASCII_DIR']) / ascii_asset
    with open(path, 'r', encoding='utf-8') as file:
        ascii_str = file.read()
    return ascii_str

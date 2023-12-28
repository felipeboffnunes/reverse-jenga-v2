import json


def is_valid_json(line):
    try:
        json.loads(line)
        return True
    except json.JSONDecodeError:
        return False

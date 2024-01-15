import json


def convert_json_to_dict(json_path: str) -> dict:
    """Opens json file and converts it to dict."""
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

import json
import os

def get_user_settings() -> dict:
    with open(os.path.join(os.path.dirname(__file__), 'settings', 'data.json'), 'r') as f:
        data = json.load(f)
        return data

def write_user_settings(data) -> None:
    with open('settings/data.json', 'w') as f:
        json.dump(data, f, indent=4)
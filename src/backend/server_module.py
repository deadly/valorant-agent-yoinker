import json

def get_user_settings() -> dict:
    with open('backend/settings/data.json', 'r') as f:
        data = json.load(f)
        return data

def write_user_settings(data) -> None:
    with open('backend/settings/data.json', 'w') as f:
        json.dump(data, f, indent=4)
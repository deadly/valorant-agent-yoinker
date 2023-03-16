import json
import os
import sys

def get_path_to_settings() -> str:
    if getattr(sys, 'frozen', False):
        # update the frontend path accordingly if running the compiled version
        return os.path.join(sys._MEIPASS, 'src', 'backend', 'settings', 'data.json')
    else:
        return os.path.join(os.path.dirname(__file__), 'settings', 'data.json')

def get_user_settings() -> dict:
    with open(get_path_to_settings(), 'r') as f:
        data = json.load(f)
        return data

def write_user_settings(data: dict) -> None:
    with open(get_path_to_settings(), 'w') as f:
        json.dump(data, f, indent=4)
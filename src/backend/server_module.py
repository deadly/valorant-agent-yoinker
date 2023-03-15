import json

def get_user_settings():
    with open('data.json', 'r') as f:
        data = json.load(f)
        return data

def write_user_settings(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
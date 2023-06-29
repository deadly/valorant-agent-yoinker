import json
import os
import sys
import requests

# get map preferences and program settings from data.json
def get_user_settings() -> dict:
    with open("settings/data.json", 'r') as f:
        data = json.load(f)
        return data

# rewrite data.json with updated map preferences and settings
def write_user_settings(data: dict) -> None:
    with open("settings/data.json", 'w') as f:
        json.dump(data, f, indent=4)

# create file named after profile that contains preferences
def create_user_profile(data: dict, name: str) -> None:
    with open(f"settings/profiles/{name}.json", 'w') as f:
        json.dump(data, f, indent=4)

# return the preferences from a file named after the selected profile
def get_user_profile(name: str) -> dict:
    with open(f"settings/profiles/{name}.json", 'r') as f:
        data = json.load(f)
        return data
    
# return the names of all created profiles    
def get_profile_names() -> list:
    files = os.listdir("settings/profiles")
    return [file.replace('.json', '') for file in files]

def get_agents() -> dict:
    # request all information for current agents then create a dictionary of name to uuid
    agentsMap = {}
    agentsData = requests.get("https://valorant-api.com/v1/agents", params={'isPlayableCharacter': True}).json()['data']
    
    for agent in agentsData:
        agentsMap[agent['displayName']] = agent['uuid']

    return {'None': 'None', **dict(sorted(agentsMap.items()))}

def get_maps() -> dict:
    # request all information for maps and create a dictionary of mapUrl to displayName

    maps = {}
    mapsData = requests.get("https://valorant-api.com/v1/maps").json()['data']
    mapJSONData = get_user_settings()

    for mapInfo in mapsData:
        if (mapInfo['displayName'] == 'The Range'):
            continue

        if (mapInfo['mapUrl'] not in mapJSONData['mapPreferences'].keys()):
            mapJSONData['mapPreferences'][mapInfo['mapUrl']] = None
            write_user_settings(mapJSONData)

        maps[mapInfo['mapUrl']] = mapInfo['displayName'] # create a dictionary in map codename:map displayname format
    
    return maps

def get_regions() -> dict:
    return [
        "NA", 
        "EU",
        "LATAM",
        "BR",
        "AP",
        "KR",
        "PBE"
    ]
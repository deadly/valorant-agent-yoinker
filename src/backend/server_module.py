import json
import os
import sys
import requests

def get_user_settings() -> dict:
    with open("settings/data.json", 'r') as f:
        data = json.load(f)
        return data

def write_user_settings(data: dict) -> None:
    with open("settings/data.json", 'w') as f:
        json.dump(data, f, indent=4)

def get_agents() -> dict:
    # request all information for current agents then create a dictionary of name to uuid
    agentsMap = {'None': 'None'}
    agentsData = requests.get("https://valorant-api.com/v1/agents", params={'isPlayableCharacter': True}).json()['data']
    
    for agent in agentsData:
        agentsMap[agent['displayName']] = agent['uuid']

    return agentsMap

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
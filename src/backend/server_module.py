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
    # request all information for current agents then create a map of name to uuid
    agentsMap = {}
    agentsData = requests.get("https://valorant-api.com/v1/agents", params={'isPlayableCharacter': True}).json()['data']
    
    for agent in agentsData:
        agentsMap[agent['displayName']] = agent['uuid']
    
    return agentsMap

def get_maps() -> dict:
    mapCodes =  {
        "Ascent": "ascent",
        "Bind": "duality",
        "Breeze": "foxtrot",
        "Fracture": "canyon",
        "Haven": "triad",
        "Icebox": "port",
        "Pearl": "pitt",
        "Split": "bonsai",
        "Lotus": "jam"
    }
    
    # request all information for maps and create a dictionary

    maps = {}
    mapsData = requests.get("https://valorant-api.com/v1/maps").json()['data']

    for mapInfo in mapsData:
        if (mapInfo['displayName'] == 'The Range'):
            continue

        maps[mapInfo['displayName']] = mapCodes[mapInfo['displayName']] # create a dictionary in map name:map code format
    
    return maps
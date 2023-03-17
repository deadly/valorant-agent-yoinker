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
        "ascent": "ascent",
        "bind": "duality",
        "breeze": "foxtrot",
        "fracture": "canyon",
        "haven": "triad",
        "icebox": "port",
        "pearl": "pitt",
        "split": "bonsai",
        "lotus": "jam"
    }

    
    # request all information for maps and then create a dictionary containing 


    maps = {}
    mapsData = requests.get("https://valorant-api.com/v1/maps").json()['data']

    for map in mapsData:
        maps[map['']]
        #not gonna change it but you should use something like _map or find a diff name just better practice
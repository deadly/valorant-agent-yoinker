import json
import requests
from valclient.client import Client

print('Valorant Agent Yoinker by https://github.com/deadly')
valid = False
agents = {}
seenMatches = []
choice = ''

def findMapName(id):
    r = requests.get(f"https://valorant-api.com/v1/maps/{id}")
    data = r.json()
    return data['data']['displayName']

with open('data.json', 'r') as f:
    data = json.load(f)
    agents = data['agents']
    maps = data['maps']
    ranBefore = data['ran']
    mapCodes = data['codes']
    region = data['region']


if (ranBefore == True):
        choice = input("type S to start or type C to change preferred agents: ").lower()

if (ranBefore == False or choice == 'c'): 
    playerRegion = input('Enter your region (e.g NA): ').lower()
    client = Client(region=playerRegion)
    client.activate()

    
    print("\nPlease Enter Preferred Agent For Each Map (e.g kayo)")
    print("_________________________________________________________\n")

    for map in maps.keys():
        valid = False
        while valid == False:
            try:
                preferredAgent = input(f"Preferred agent on {mapCodes[map].capitalize()}: ").lower()
                if (preferredAgent in agents.keys()):
                    maps[map] = agents[preferredAgent]
                    valid = True
                else:
                    print("Invalid Agent")
            except:
                print("Input Error")
    
    with open('data.json', 'w') as f:
            data['maps'] = maps
            data['ran'] = True
            data['region'] = playerRegion
            json.dump(data, f)

else:
    client = Client(region=region)
    client.activate()


print("Waiting for Agent Select\n")
while True:
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        matchID = client.pregame_fetch_match()['ID']
        if ((sessionState == "PREGAME") and (matchID not in seenMatches)):
            matchInfo = client.pregame_fetch_match(matchID)
            mapName = matchInfo["MapID"].split('/')[-1].lower()
            print(f'Agent Select Found - {mapCodes[mapName].capitalize()}')

            client.pregame_select_character(maps[mapName])
            client.pregame_lock_character(maps[mapName])
            seenMatches.append(client.pregame_fetch_match()['ID'])
            print('Agent Locked - ' + list(agents.keys())[list(agents.values()).index(maps[mapName])].capitalize())

    except Exception as e:
        print('', end='') # Using pass caused weird behavior

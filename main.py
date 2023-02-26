import json, time
from valclient.client import Client

print('Valorant Agent Yoinker by https://github.com/deadly')
valid = False
running = True
agents = {}
seenMatches = []
choice = ''

with open('data.json', 'r') as f:
    data = json.load(f)
    agents = data['agents']
    maps = data['maps']
    ranBefore = data['ran']
    mapCodes = data['codes']
    region = data['region']
    hoverDelay = data['hoverDelay']
    lockDelay = data['lockDelay']


if (ranBefore == True):
        choice = input("type S to start or type C to change preferred agents: ").lower()

if (ranBefore == False or choice == 'c'): 
    playerRegion = input('Enter your region (e.g NA): ').lower()
    client = Client(region=playerRegion)
    client.activate()

    
    print("\nPlease Enter Preferred Agent For Each Map (type NONE to not instalock on a map)")
    print("_"*80, end="\n")

    for map in maps.keys():
        valid = False
        while valid == False:
            try:
                preferredAgent = input(f"Preferred agent on {mapCodes[map].capitalize()}: ").lower()
                if (preferredAgent in agents.keys()):
                    maps[map] = agents[preferredAgent]
                    valid = True
                elif (preferredAgent == "none"):
                    maps[map] = None
                    valid = True
                else:
                    print("Invalid Agent")
            except Exception as e:
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
while running:
    time.sleep(5)
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        matchID = client.pregame_fetch_match()['ID']

        if (sessionState == "PREGAME" and matchID not in seenMatches):
            seenMatches.append(matchID)
            matchInfo = client.pregame_fetch_match(matchID)
            mapName = matchInfo["MapID"].split('/')[-1].lower()
            side = lambda teamID: "Defending" if teamID == "Blue" else "Attacking"
            
            print(f'Agent Select Found - {mapCodes[mapName].capitalize()} - ' + side(matchInfo['Teams'][0]['TeamID']) + ' first')
            if (maps[mapName] != None):
                time.sleep(hoverDelay)
                client.pregame_select_character(maps[mapName])
                time.sleep(lockDelay)
                client.pregame_lock_character(maps[mapName])
                print('Agent Locked - ' + list(agents.keys())[list(agents.values()).index(maps[mapName])].capitalize())
    except Exception as e:
        if "pre-game" not in str(e):
            print("An error occurred:", e)

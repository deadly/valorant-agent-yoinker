import json, time
import requests
from valclient.client import Client
from zipfile import ZipFile
import os
import shutil


print('Valorant Agent Yoinker by https://github.com/deadly')
VERSION = 1.3
valid = False
running = True
agents = {}
seenMatches = []
choice = ''

print(os.listdir())
if "Agent Yoinker U.exe" in os.listdir():
    if "Agent Yoinker.exe" in os.listdir():
        os.remove("Agent Yoinker.exe")
    os.rename("Agent Yoinker U.exe", "Agent Yoinker.exe")
    print("in")

with open('data.json', 'r') as f:
    data = json.load(f)
    update = data["checkUpdates"]
    agents = data['agents']
    maps = data['maps']
    ranBefore = data['ran']
    mapCodes = data['codes']
    region = data['region']
    hoverDelay = data['hoverDelay']
    lockDelay = data['lockDelay']
    loopDelay = data['loopDelay']

if update == True:
    try:
        updatedata = requests.get("https://api.github.com/repos/deadly/valorant-agent-yoinker/releases/latest").json()
        latest = float(updatedata["tag_name"].split("-")[1])
    except Exception as e: #requests.ConnectionError
        raise e
        print("An error occured while checking for updates.")
    else:
        if VERSION != latest:
            uchoice = input("There is a newer version would you like to update? (y or n): ").lower()
            if uchoice == "y":
                print("UPDATING...")
                with open("temp.zip", "wb") as f:
                    f.write(requests.get(updatedata["assets"][0]["browser_download_url"]).content)
                
                with ZipFile("temp.zip", "r") as zfo:
                    zfo.extractall("./t")
                os.remove("temp.zip")
                base = "t/"+os.listdir("t")[0]
                with open("data.json", "wb") as wf:
                    with open(f"./{base}/data.json", "rb") as rf:
                        wf.write(rf.read())
                
                with open("Agent Yoinker U.exe", "wb") as wf:
                    with open(f"./{base}/Agent Yoinker.exe", "rb") as rf:
                        wf.write(rf.read())
                shutil.rmtree("t")

                os.startfile("Agent Yoinker U.exe")
                os._exit(1)





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
    time.sleep(loopDelay)
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

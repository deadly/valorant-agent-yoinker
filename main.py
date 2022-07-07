import json
from requests import session
from valclient.client import Client
print('Valorant Agent Yoinker by https://github.com/deadly')
playerRegion = input('Enter your region (see Github page): ').lower()
client = Client(region=playerRegion)
client.activate()
valid = False
agents = {}
seenMatches = []

with open('data.json', 'r') as f:
    agents = json.load(f)

while valid == False:
    try: 
        preferredAgent = input("Preferred Agent (e.g Kayo): ").lower()
        if (preferredAgent in agents['agents'].keys()):
            valid = True
        else:
            print("Invalid Agent")
    except:
        print("Input Error")

print("Waiting for Agent Select")
while True:
    try:
        sessionState = client.fetch_presence(client.puuid)['sessionLoopState']
        if ((sessionState == "PREGAME") and (client.pregame_fetch_match()['ID'] not in seenMatches)):
            print('Agent Select Found')
            client.pregame_select_character(agents['agents'][preferredAgent])
            client.pregame_lock_character(agents['agents'][preferredAgent])
            seenMatches.append(client.pregame_fetch_match()['ID'])
            print('Successfully Locked ' + preferredAgent.capitalize())
    except Exception as e:
        print('', end='')
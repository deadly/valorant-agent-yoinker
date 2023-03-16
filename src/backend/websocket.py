import asyncio
import ssl
import websockets
import base64
import os
import requests


lockfile = {}
pregameMsg = "/riot-messaging-service/v1/message/ares-pregame/pregame/v1/matches/"

try:
    with open(os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')) as lockfile:
        data = lockfile.read().split(':')
        keys = ['name', 'PID', 'port', 'password', 'protocol']
        lockfile = dict(zip(keys, data))
except:
    raise Exception("Lockfile could not be found")



# CREDIT TO https://github.com/OwOHamper/ FOR WEBSOCKET SKELETON CODE

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

local_headers = {}
local_headers['Authorization'] = 'Basic ' + base64.b64encode(('riot:' + lockfile['password']).encode()).decode()
url = f"wss://127.0.0.1:{lockfile['port']}"

# dictionary with important values for the websocket to use
wsInfo = {'port': '','running': False}

async def ws():
    global wsInfo
    flaskURL = f'http://127.0.0.1:{wsInfo["port"]}'
    async with websockets.connect(url, ssl=ssl_context, extra_headers=local_headers) as websocket:
        
        await websocket.send("[5, \"OnJsonApiEvent\"]")

        while wsInfo['running']:
            response = await websocket.recv()
            if len(response) > 0:
                if pregameMsg in response:
                    requests.get(f'http://127.0.0.1:{wsInfo["port"]}/pregame_found')
        
        
def startWs(port):
    global wsInfo
    wsInfo['running'] = True
    wsInfo['port'] = port
    asyncio.run(ws())

def closeWs():
    global wsInfo
    wsInfo['running'] = False


import webview
from backend.server import server
from backend.websocket import startWs, closeWs
from websockets.exceptions import ConnectionClosedError

def initWS(window):
    try:
        startWs(window.get_current_url().replace('/','').replace('region', '').split(':')[2]) # start the ws and pass the port of the server
    except ConnectionClosedError:
        pass
        #TODO: Send user a page saying they closed valorant. Have a button on this page to restart websocket when they launch again.
    except Exception as e:
        raise e


window = webview.create_window('Agent Yoinker', server, height=720, width=1280)
webview.start(initWS, (window,)) # start the window along with startWs in a separate thread
closeWs()
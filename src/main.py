import webview
from backend.server import server
from backend.websocket import startWs, closeWs

def initWS(window):
    startWs(window.get_current_url().replace('/','').split(':')[2]) # start the ws and pass the port of the server

window = webview.create_window('Agent Yoinker', server, height=720, width=1280)
webview.start(initWS, (window,)) # start the window along with startWs in a separate thread
closeWs()
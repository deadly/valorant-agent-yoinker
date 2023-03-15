import webview
from backend.server import server
from backend.websocket import startWs, closeWs


window = webview.create_window('Agent Yoinker', server, height=720, width=1280)
webview.start(startWs, debug=True) # start the window along with startWs in a separate thread
closeWs()
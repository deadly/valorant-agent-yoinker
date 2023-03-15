import webview
from backend.server import server
from backend.websocket import startWs

window = webview.create_window('Agent Yoinker', server)
webview.start(startWs) # start the window along with startWs in a separate thread
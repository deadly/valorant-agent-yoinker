import webview
from backend.server import server

webview.create_window('Agent Yoinker', server)
webview.start()
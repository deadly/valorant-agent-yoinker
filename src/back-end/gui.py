import webview
from server import server

webview.create_window('Agent Yoinker', server)
webview.start()
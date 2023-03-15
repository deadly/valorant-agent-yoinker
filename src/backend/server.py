import os, sys
from flask import Flask, render_template
from valclient.client import Client
from backend.player import Player

# creates client and player object
client = Client(region='na')
client.activate()
player = Player(client=client)

# path for files for front-end
guiDir = os.path.join(os.path.dirname(__file__), '..', 'frontend')

if getattr(sys, 'frozen', False):
    guiDir = os.path.join(sys._MEIPASS, 'src', 'frontend')
    print(sys._MEIPASS)
    server = Flask(__name__, static_folder=guiDir, template_folder=guiDir)
else:
    server = Flask(__name__, static_folder=guiDir, template_folder=guiDir)

@server.route("/")
def home():
    return render_template('index.html', name=player.name)
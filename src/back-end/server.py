import os
from flask import Flask, render_template
from valclient.client import Client
from player import Player

# creates client and player object
client = Client(region='na')
client.activate()
player = Player(client=client)

# path for files for front-end
guiDir = os.path.join(os.path.dirname(__file__), '..', 'front-end')

server = Flask(__name__, static_folder=guiDir, template_folder=guiDir)

@server.route("/")
def home():
    return render_template('index.html', name=player.name)
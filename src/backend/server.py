import os, sys
from flask import Flask, render_template
from valclient.client import Client
from backend.player import Player


# creates client and player object
client = Client(region='na')
client.activate()
player = Player(client=client)

# initialization variables
firstReq = True # variable to keep track if GET / has been seen before

# path for files for front-end
guiDir = os.path.join(os.path.dirname(__file__), '..', 'frontend')

if getattr(sys, 'frozen', False):
    # update the frontend path accordingly if running the compiled version
    guiDir = os.path.join(sys._MEIPASS, 'src', 'frontend')

server = Flask(__name__, static_folder=guiDir, template_folder=guiDir)
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable caching



@server.route("/")
def home():
    global firstReq
    
    return render_template('index.html', name=player.name)

@server.route("/settings")
def settings():
    return render_template("settings.html", name=player.name)
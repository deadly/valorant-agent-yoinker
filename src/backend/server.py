import os, sys
from flask import Flask, render_template
from valclient.client import Client
from backend.player import Player
from backend.server_module import get_user_settings


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

data = get_user_settings()

@server.context_processor
def inject_name():
    return dict(name=player.name) #makes it so we dont have to pass name every time

@server.route("/")
def home():
    global firstReq
    
    return render_template('index.html')

@server.route("/settings")
def settings():
    keys = [i for i in data.keys()]
    values = [i for i in data.values()]
    return render_template("settings.html", keys=keys, values=values)

# endpoint that gets request when websocket encounters pregame
@server.route("/pregame_found", methods=['GET'])
def pregame_found():
    print("the websocket has encountered pregame")
    return '', 204

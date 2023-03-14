import os
from flask import Flask, render_template, request
from valclient.client import Client
from player import Player
import json

with open("settings/data.json", "r") as f:
    data:dict = json.loads(f.read())

def update_config():
    with open("settings/data.json", "r") as f:
        data = json.loads(f.read())



def save_config():
    with open("settings/data.json", "w") as f:
        json.dump(data, f, indent=4)



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

print(data)

@server.route("/config", methods=["GET", "POST"])
def config():
    keys = [i for i in data.keys()]
    values = [i for i in data.values()]
    if request.method == "POST":
        
        print(request.form.get())
    
    return render_template("config.html",
                           keys=keys,
                           values=values)


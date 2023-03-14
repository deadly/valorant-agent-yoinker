import os
from flask import Flask, render_template, request
from valclient.client import Client, HandshakeError
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
player = None


# path for files for front-end
guiDir = os.path.join(os.path.dirname(__file__), '..', 'front-end')

server = Flask(__name__, static_folder=guiDir, template_folder=guiDir)




@server.route("/")
def home():
    if not player:
        try:
            client.activate()
            player = Player(client=client)
        except HandshakeError:
            return server.redirect("/openval")
    return render_template('index.html', name=player.name)



@server.route("/openval", methods=["GET", "POST"])
def open_val():
    hiddenerror = "Val is still not open"
    if request.method == "POST":
        try:
            client.activate()
            player = Player(client=client)
        except HandshakeError:
            hiddenerror += "!"
            return render_template("valnotopen.html", hiddenerror=hiddenerror)
        else:
            return server.redirect("/")
    return render_template("valnotopen.html")


@server.route("/config", methods=["GET", "POST"])
def config():
    keys = [i for i in data.keys()]
    values = [i for i in data.values()]
    if request.method == "POST":
        
        print(request.form.get())
    
    return render_template("config.html",
                           keys=keys,
                           values=values)


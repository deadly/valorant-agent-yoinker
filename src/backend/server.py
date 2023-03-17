import os, sys
from flask import Flask, render_template, request
from valclient.client import Client
from backend.player import Player
from backend.server_module import get_user_settings, write_user_settings, get_agents, get_maps


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

@server.route("/", methods=('GET', 'POST'))
def home():
    global firstReq
    if request.method == 'POST':
        allsettings = get_user_settings()
        mapsettings = allsettings['mapPreferences']
        for _map in mapsettings.keys():
            req = request.form[_map]
            if req.lower() == "none":
                req = None
            mapsettings[_map] = req
        write_user_settings(allsettings)
    settings = get_user_settings()['mapPreferences'].items()
    return render_template('index.html', settings=settings, agents=get_agents(), maps=get_maps())

@server.route("/settings", methods=('GET', 'POST'))
def settings():
    settings = data.items()
    if request.method == 'POST':
        # get new settings from post request then update data
        checkUpdates = request.form['checkUpdates'] #need to make this a checkbox or dropdown | True or False
        hoverDelay = int(request.form['hoverDelay'])
        lockDelay = int(request.form['lockDelay'])
        data['checkUpdates'] = checkUpdates if checkUpdates != '' else data['checkUpdates'] 
        data['hoverDelay'] = hoverDelay if hoverDelay != '' else data['hoverDelay']
        data['lockDelay'] = lockDelay if lockDelay != '' else data['lockDelay']
        write_user_settings(data)

    return render_template("settings.html", settings=settings)

# requested endpoint when websocket encounters pregame
@server.route("/pregame_found", methods=['GET'])
def pregame_found():
    print("the websocket has encountered pregame")
    return '', 204

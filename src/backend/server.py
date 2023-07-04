import os, sys, time, json
from flask import Flask, render_template, request, url_for, redirect
from valclient.client import Client
from valclient.exceptions import HandshakeError
from backend.player import Player
from backend.server_module import *

VERSION = 2.0
# creates client and player object
client = ''
player = ''
# initialization variables
toggle_on = True # keep track of instalock toggle
firstReq = True # variable to keep track if GET / has been seen before
currentMap = "Map"
currentTeam = "First Side"
# path for files for front-end
guiDir = os.path.join(os.path.dirname(__file__), '..', 'frontend')

if getattr(sys, 'frozen', False):
    # update the frontend path accordingly if running the compiled version
    guiDir = os.path.join(sys._MEIPASS, 'src', 'frontend')

server = Flask(__name__, static_folder=guiDir, template_folder=guiDir)
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable caching

data = get_user_settings()

def init_player():
    global client, player

    client = Client(region=data['region'].lower())
    client.activate()
    player = Player(client=client)

@server.context_processor
def inject_name():
    try:
        return dict(name=player.name) #makes it so we dont have to pass name every time
    except:
        return dict(name='Set Region')


@server.route("/region", methods=('GET', 'POST'))
def regionPopup():
    if request.method == 'POST':
        region = request.form['region']
        data['region'] = region
        write_user_settings(data)
        return redirect('/')
    return render_template('region.html', regions=get_regions())

@server.route('/valorant_closed', methods=("GET", "POST"))
def valorant_closed():
    if request.method == 'POST':
        return redirect("/")
    return render_template('valorantclosed.html')

@server.route('/update_found', methods=('GET', 'POST'))
def update_found():
    if request.method == 'POST':
        if request.form['update'] == 'true':
            print("true")
            #TODO: actually update the app
        else:
            return redirect("/")
    return render_template('updatefound.html')

@server.route("/", methods=('GET', 'POST'))
def home():
    global firstReq

    if data['checkUpdates'] == True:
        if check_updates(VERSION):
            return redirect("update_found")

    if data['region'] == None:
        return redirect('region')
    elif (firstReq == True) and (data['region'] != None):
        try:
            init_player()
        except HandshakeError:
            return redirect('valorant_closed')
    
    firstReq = False

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
    maps = get_maps()

    return render_template(
        'index.html', 
        settings=settings,
        agents=get_agents(), 
        maps=maps,
        toggle_on=toggle_on,
        currentMap=currentMap,
        currentTeam=currentTeam
    )

@server.route("/settings", methods=('GET', 'POST'))
def settings():
    settings = data.items()
    if request.method == 'POST':
        # get new settings from post request then update data
        checkUpdates = request.form['checkUpdates'] # need to make this a checkbox or dropdown | True or False
        region = request.form['region']
        hoverDelay = int(request.form['hoverDelay'])
        lockDelay = int(request.form['lockDelay'])
        data['checkUpdates'] = True if checkUpdates.lower() == "true" else False
        data['region'] = region if region in get_regions() else data['region']
        data['hoverDelay'] = hoverDelay if hoverDelay != '' else data['hoverDelay']
        data['lockDelay'] = lockDelay if lockDelay != '' else data['lockDelay']
        
        write_user_settings(data)
    return render_template("settings.html", settings=settings, regions=get_regions())

@server.route("/info")
def info():
    return render_template("info.html")

# requested endpoint when websocket encounters pregame
@server.route("/pregame_found", methods=['GET'])
def pregame_found():
    try:
        if toggle_on:
            settings = get_user_settings()
            agents = get_agents()
            player.acknowledge_current_match()
            preferredAgent = agents[settings['mapPreferences'][player.currentMatch['map']]]

            time.sleep(settings['hoverDelay'])
            player.hover_agent(preferredAgent)
            time.sleep(settings['lockDelay'])
            player.lock_agent(preferredAgent)
        return '', 200
    except Exception as e:
        print("Unknown error:", e)
        return '', 204

@server.route("/get_match_info", methods=['GET'])
def get_match_info():
    try:
        return player.get_current_match()
    except Exception as e:
        return '', 204

@server.route("/get_seen_matches", methods=['GET'])
def get_seen_matches():
    try:
        return player.get_seen_matches()
    except Exception as e:
        print('Unknown error', e)
        return '', 204
    
@server.route('/toggle', methods=['GET', 'POST'])
def toggle():
    global toggle_on
    toggle_on = not toggle_on
    return '', 200

@server.route('/updateMapTeam', methods=['GET'])
def updateMapTeam():
    sideMap = player.get_side_map()
    if (sideMap):
        sideMap[0] = get_maps()[sideMap[0]]
        return sideMap
    return '', '204'

@server.route('/create_profile', methods=['POST'])
def createProfile():
    try:
        profile = request.json.get('profilePreferences')
        name = request.json.get('name')

        create_user_profile(profile, name)
    except Exception as e:
        print("Error saving profile: ", e)

    return '', '204'

@server.route('/fetch_profiles', methods=['GET'])
def fetchProfiles():
    return get_profile_names()

@server.route('/fetch_profile_settings', methods=['GET'])
def fetchProfileSettings():
    try:
        return get_user_profile(request.args.get('selectedValue'))
    except Exception as e:
        print("Error fetching profile settings: ", e)
    
    return '', '204'


import time
import game_elements as ge
from valclient.client import Client

def get_match_map_name(match_info: dict) -> str:
    game_map = match_info["MapID"].split('/')[-1].lower()
    for item in ge.Map:
        if item.value == game_map:
            return item.name.lower()
        
def get_match_game_mode_name(match_info: dict) -> str:
    competitive = match_info["QueueID"]  # can be either "competitive" or ""
    game_mode = match_info["Mode"].split('/')[-2].lower() + competitive
    for item in ge.GameMode:
        if item.value == game_mode:
            return item.name.lower()

# TODO: Make the actual instalocker
def instalocker(region: str, selected_set: dict):
    client = Client(region=region)
    client.activate()
    
    while True:
        time.sleep(2)

        try:
            match_info = client.pregame_fetch_match()
            break
        except Exception as e:
            if "pre-game" not in str(e):
                print("e")
    
    # check for game mode
    set_game_mode = list(selected_set.keys())[1]
    if get_match_game_mode_name(match_info) == set_game_mode.lower():
        # get the match map name
        match_map = get_match_map_name(match_info).upper()
        
        # use the match map name to get a map object
        map_object = ge.Map.__members__[match_map]
        
        # use the map object to get the agent value (id)
        desired_agent = selected_set[set_game_mode][map_object.name.title()]
        
        # lock the character
        client.pregame_lock_character(desired_agent)  # TODO: finish this
        
    return
                

    
def main() -> int:
    instalocker('br', None)
    return 0


if __name__ == '__main__':
    main()

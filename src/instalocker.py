import time

from valclient.client import Client

import game_elements as ge
import profile_handler as ph


def instalocker(region: str, profile: ph.Profile) -> bool:
    """Instalock a agent.

    Args:
        region (str): The user server region.
        profile (ph.Profile): The user profile

    Returns:
        bool: True is the agent was successfully instalocked, False otherwise.
    """
    # Start client
    client = Client(region)
    client.activate()

    while True:
        # TODO: Add a timeout to prevent while loop to run indefinitely

        # loop delay to reduce API calls
        time.sleep(2)  # TODO: make this value variable

        try:
            # If pregame_fetch_match does not raise a error it means that the player is in a pre-game
            match_info = client.pregame_fetch_match()
            break
        except Exception as e:
            # Check if the error is a pre-game error or other error
            # TODO: make check with the actual Exception class
            if "pre-game" not in str(e):
                print("e")

    # If out of the while loop the player is in a pre-game.
    # It means that pre-game functions should not raise any error (at least related to pre-game)

    # Check the game mode
    match_game_mode = get_match_game_mode(match_info)
    if match_game_mode == profile.game_mode:
        # Get the agent for the map
        agent = profile.map_agent[get_match_map(match_info)]

        # check if the user wants to instalock in this map
        if agent is None:
            return False

        # Instalock the character
        # TODO: check if the character was successfully instalocked to return True of False
        client.pregame_lock_character(agent.value)

    return True


def get_match_game_mode(match_info: dict) -> ge.GameMode:
    """Get a game mode object from the match information.

    Args:
        match_info (dict): Match information. The return of the valclient.client.Client.pregame_fetch_match()

    Returns:
        ge.GameMode: The game mode
    """
    # TODO: finish this function and use correct return
    game_mode = match_info['Mode']
    print(game_mode)

    return ge.GameMode.COMPETITIVE


def get_match_map(match_info: dict) -> ge.Map:
    """Get a map object from the match information.

    Args:
        match_info (dict): Match information. The return of the valclient.client.Client.pregame_fetch_match()

    Returns:
        ge.Map: The map
    """
    # TODO: finish this function and use correct return
    game_map = match_info['MapID']  # .split('/')[-1].lower()
    print(game_map)

    return ge.Map.ASCENT


def main() -> int:
    instalocker('br', ph.load_profile('test'))
    return 0


if __name__ == '__main__':
    main()

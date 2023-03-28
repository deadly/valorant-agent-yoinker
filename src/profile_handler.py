"""This file is called 'profile_handler' because the name 'profile' overrides the stdlib module 'profile'"""

import dataclasses
import json
import os

import constants as const
import game_elements as ge


@dataclasses.dataclass
class Profile:
    name: str
    game_mode: ge.GameMode
    map_agent: dict[ge.Map, ge.Agent | None]


def load_profile(profile_name: str) -> Profile:
    """Load the information of a profile file.

    If the profile does not exist, an error will occur.

    Args:
        profile_name (str): The name of the profile.

    Returns:
        Profile: The profile object containing the information from the file.
    """
    # Load JSON data from file
    with open(const.PROFILE_PATH + profile_name + '.json', 'r') as f:
        json_data = json.load(f)

    # Create instances of dataclasses using JSON data
    # Use Enum to get enum member
    game_mode = ge.GameMode[json_data['game_mode'].upper()]
    map_agent = {ge.Map[k.upper()]: (ge.Agent[v.upper()] if v is not None else None)
                 for k, v in json_data['map_agent'].items()}
    return Profile(profile_name, game_mode, map_agent)


def dump_profile(game_data: Profile) -> None:
    """Dump information from a profile object into a file.

    Args:
        game_data (Profile): The profile object with will be dumped into the file.
    """
    # Dump dataclass instances to JSON
    game_data_dict = {
        'game_mode': game_data.game_mode.name.title(),
        'map_agent': {k.name.title(): (v.name.title() if v is not None else None) for k, v in game_data.map_agent.items()}
    }
    with open(const.PROFILE_PATH + game_data.name + '.json', 'w') as f:
        json.dump(game_data_dict, f, indent=4)


def delete_profile(profile_name: str) -> None:
    """Delete the profile file with the given name.

    Args:
        profile_name (str): The profile name (no file extension).
    """
    os.remove(f'{const.PROFILE_PATH}\\{profile_name}.json')

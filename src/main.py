import easygui as eg
import os
import game_elements as ge
import json
import typing as t
import dataclasses

PROFILE_PATH = os.path.join(os.getcwd(), 'profiles/')

# TODO: make this a dictionary. implement regions locations and names
# https://support-valorant.riotgames.com/hc/en-us/articles/360055678634-Server-Select
REGIONS = ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

# TODO: move this Profile class and related functions to different files


@dataclasses.dataclass
class Profile:
    name: str
    game_mode: ge.GameMode
    map_agent: t.Dict[ge.Map, ge.Agent | None]


def load_profile(profile_name: str) -> Profile:
    """Load the information of a profile file.

    If the profile does not exist, an error will occur.

    Args:
        profile_name (str): The name of the profile.

    Returns:
        Profile: The profile object containing the information from the file.
    """
    # Load JSON data from file
    with open(PROFILE_PATH + profile_name + '.json', 'r') as f:
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
    with open(PROFILE_PATH + game_data.name + '.json', 'w') as f:
        json.dump(game_data_dict, f, indent=4)


def delete_profile(profile_name: str) -> None:
    """Delete the profile file with the given name.

    Args:
        profile_name (str): The profile name (no file extension).
    """
    os.remove(f'{PROFILE_PATH}\\{profile_name}.json')


class UserSettings(eg.EgStore):
    def __init__(self, filename: str) -> None:  # filename is required
        # Specify default/initial values for variables that an application wants to remember.
        self.region: str | None = None
        self.profile: Profile | None = None

        # For subclasses of EgStore, these must be the last two statements in the __init__ method
        self.filename = filename
        self.restore()


# TODO: rename this class to "App" or similar
class Instalocker:
    def __init__(self, region: str | None = None, profile: Profile | None = None) -> None:
        # TODO: implement the settings set and recovering using the UserSettings class.
        # make region and profile setter (and getter if needed) methods
        self.region: str | None = region
        self.profile: Profile | None = profile
        # TODO: make a "main_loop" function to handle the infinite loop

    def main_menu(self) -> bool:
        """The main options of the application.

        Show options to the user depending on some criteria

        Returns:
            bool: True if the user selected a option, False if the user canceled the action.
        """
        # Define the available options depending on some criteria
        no_region = {
            'message': 'You haven\'t selected your region. Select a region to use Valorant instalocker',
            'choices': {
                'Region': self.region_menu
            }
        }
        no_profile_created = {
            'message': 'You have no profile created. Create a profile to use Valorant instalocker',
            'choices': {
                'Create new profile': self.create_profile_menu,
                **no_region['choices']
            }
        }
        no_profile_selected = {
            'message': 'You have no profile selected. Select a profile to use Valorant instalocker',
            'choices': {'Select profile': self.select_profile_menu,
                        'Delete profile': self.delete_profile_menu,
                        **no_profile_created['choices']
                        }
        }
        has_profile_and_region = {
            'message': 'Selected profile: {profile_name}',
            'choices': {'Start instalocker': self.start_instalocker_menu,
                        **no_profile_selected['choices']
                        }
        }

        # Define the options according to the criteria
        # Does not have a region.
        if not self.region:
            info = no_region

        # Does not have any profile created and has region.
        elif not check_any_profile_existence():
            info = no_profile_created

        # Has at least one profile created but none is selected and has region.
        elif not self.profile:
            info = no_profile_selected

        # Has a selected profile and has region.
        else:
            # Add the profile name
            has_profile_and_region['message'] = has_profile_and_region['message'].format(
                profile_name=self.profile.name.title())
            info = has_profile_and_region

        # get the input from the user
        msg = info['message'] + '\n\nPick a option'
        available_choices = info['choices']
        user_choice = eg.choicebox(
            msg, 'Main Menu', list(available_choices.keys()))

        # User canceled the operation
        if user_choice is None:
            return False

        # Call the choice option and return
        info['choices'][user_choice]()
        return True

    def region_menu(self) -> bool:
        """Set the instance region.

        Returns:
            bool: True if a new regions was set, False otherwise
        """
        if user_region := get_region('Select your region'):
            self.region = user_region
            # TODO: save new settings
            eg.msgbox(f'Region {self.region.upper()} selected successfully!',
                      'Success')
            return True
        return False

    def create_profile_menu(self) -> bool:
        """Create a new profile file.

        Returns:
            bool: True if a new profile was created. False otherwise
        """
        if game_mode := get_game_mode('Chose the game mode for the profile'):
            if map_agent := get_map_agent(f'Type the character you like for each map in the {game_mode.name.title()} game mode.\nLeave blank if you don\'t want to instalock in that map.'):
                if profile_name := get_user_text_input('How do you what to name your profile?\n\nIf a profile with that name already exists it will be replaced with this new one.', 'Profile name'):
                    dump_profile(Profile(profile_name, game_mode, map_agent))
                    eg.msgbox(f'Profile "{profile_name}" created successfully!\nYou can select it from the "Select Profile" option in the Main Menu',
                              'Success')
                    return True
        return False

    def select_profile_menu(self) -> bool:
        """Select a profile instance variable of the user choice.

        Returns:
            bool: True if a new profile was selected, False otherwise
        """
        if profile_name := get_profile_name('Select the profile you want to use'):
            self.profile = load_profile(profile_name)
            # TODO: save new settings
            # Show profile information
            msg = f'Profile name: {self.profile.name}\n\nProfile game mode: {self.profile.game_mode.name.title()}\n\n'
            for game_map, game_character in self.profile.map_agent.items():
                msg += f'{game_map.name.title():<10}{game_character.name.title() if game_character is not None else None}\n'
            eg.msgbox(msg, 'Profile information')
            return True
        return False

    def delete_profile_menu(self) -> bool:
        """Delete a profile file.

        Also set profile instance variable to None if a profile was successfully deleted.

        Returns:
            bool: True is a profile was deleted, False otherwise.
        """
        if profile_name := get_profile_name('Select the profile you want to delete'):
            if eg.ynbox(f'Delete the profile "{profile_name}"?', 'Profile Deletion'):
                delete_profile(profile_name)
                self.profile = None
                # TODO: save new settings
                eg.msgbox(f'Profile "{profile_name}" deleted Successfully',
                          'Profile deletion')
                return True
            else:
                eg.msgbox(f'Profile {profile_name} not deleted',
                          'Profile deletion')
        return False

    def start_instalocker_menu(self):
        # TODO: implement instalocker call
        print('start_instalocker')


def check_any_profile_existence() -> bool:
    """Check there is at least one file in the profile folder.

    Returns:
        bool: True if there is at least one file, False otherwise.
    """
    return len(profiles_names()) != 0


def profiles_names() -> list[str]:
    """Return a list of all profile file names in the profile folder.

    Returns:
        list[str]: A list with all profiles names (no file extension).
    """
    return [profile_file.removesuffix('.json') for profile_file in os.listdir(PROFILE_PATH)]


def get_region(msg: str) -> str | None:
    """Get a region from the user.

    Args:
        msg (str): The message for the user.

    Returns:
        str | None: The chosen region or None if the user canceled the action. 
    """
    # TODO: format regions
    choice = eg.choicebox(msg, 'Regions', REGIONS)

    # User canceled operation or the region
    return None if choice is None else str(choice)


def get_game_mode(msg: str) -> ge.GameMode | None:
    """Get a game mode from the user.

    Args:
        msg (str): The message for the user

    Returns:
        ge.GameMode | None: The chosen game mode or None if the user canceled the action. 
    """
    # create and format options
    available_choices = [game_mode.name.replace(
        '_', ' ').title() for game_mode in ge.GameMode]
    choice = eg.choicebox(msg, 'Game modes', available_choices)

    # User canceled operation or the game mode
    return None if choice is None else ge.GameMode[str(choice).replace(' ', '_').upper()]


def get_map_agent(msg: str) -> dict[ge.Map, ge.Agent | None] | None:
    """Get a combination of map and agent from the user.

    At least one value of the dict return will be an Agent.

    Args:
        msg (str): The message for the user

    Returns:
        dict[ge.Map, ge.Agent | None] | None: None if the user canceled the action. Map-Agent combination otherwise.
    """
    maps_name = [game_map.name.title() for game_map in ge.Map]
    agents_name = [game_agent.name.title() for game_agent in ge.Agent]

    # Validate inputs
    while True:
        agents_chosen: list[str] = eg.multenterbox(
            msg, 'Map-Agent selection', maps_name)  # type: ignore
        valid = True

        # User canceled the action
        if agents_chosen is None:
            return None

        # All blank
        if all(agent == '' for agent in agents_chosen):
            eg.msgbox('You can\'t create a empty profile', 'Invalid profile')
            continue

        # Check for invalid agents
        for agent in agents_chosen:
            agent = agent.strip().title()
            if agent not in agents_name and agent != '':
                eg.msgbox(
                    f'"{agent.strip().title()}" is not a valid agent.', 'Invalid agent')
                valid = False
                break

        if valid:
            break

    # Join the two lists to make a dictionary. Also check for empty fields to be None
    return dict(zip(list(ge.Map), [ge.Agent[agent.upper()] if agent != '' else None for agent in agents_chosen]))


def get_user_text_input(msg: str, title: str) -> str | None:
    """Get a text input from the user.

    Args:
        msg (str): The message for the user.
        title (str): The title of the box.

    Returns:
        str | None: None if the user canceled the action, the input otherwise.
    """
    # Using a multenterbox, so a list of the name of the fields is needed (['']).
    # A list with a empty string so there is only the space for the user to type. (very clean)
    user_input: list[str] = eg.multenterbox(msg, title, [''])  # type: ignore

    # User canceled operation or the input.
    # Input is the first item on the list of fields name. There is only one field.
    return None if user_input is None else user_input[0]


def get_profile_name(msg: str) -> str | None:
    """Get a profile name from the user.

    Args:
        msg (str): The message for the user.

    Returns:
        str | None: The profile name or None if the user cancel the action
    """
    profiles_name = profiles_names()

    # Add empty string to avoid the easy gui error: "ValueError: at least two choices need to be specified".
    # This empty option is equivalent to clicking in cancel
    # len(profiles_name) can't be less than one, because this option only appear if the user already has a profile created
    if len(profiles_name) == 1:
        profiles_name.append('')

    user_choice = eg.choicebox(msg, 'Profile selection', profiles_name)

    # Check if the user selected the empty string
    return None if (user_choice == '' or user_choice is None) else str(user_choice)


def main() -> int:
    app = Instalocker('br')
    while True:
        do_continue = app.main_menu()
        if not do_continue:
            break
    return 0


if __name__ == '__main__':
    main()
import os

import easygui as eg

import constants as const
import game_elements as ge
import instalocker
import profile_handler as ph


class UserSettings(eg.EgStore):
    def __init__(self, filename: str) -> None:  # filename is required
        # Specify default/initial values for variables that an application wants to remember.
        self.region: str | None = None
        self.profile: ph.Profile | None = None

        # For subclasses of EgStore, these must be the last two statements in the __init__ method
        self.filename = filename
        self.restore()


class Application:
    def __init__(self, user_settings_file: str) -> None:
        # If the user_settings_file exists, this will restore its values
        self._settings = UserSettings(user_settings_file)

    @property
    def region(self) -> str | None:
        return self._settings.region

    @region.setter
    def region(self, value: str) -> None:
        self._settings.region = value
        # Save the new value on the settings file
        self._settings.store()

    @property
    def profile(self) -> ph.Profile | None:
        return self._settings.profile

    @profile.setter
    def profile(self, value: ph.Profile | None) -> None:
        self._settings.profile = value
        # Save the new value on the settings file
        self._settings.store()

    def run(self) -> None:
        """Runs the main_menu until user cancel the action on the main_menu (cancel button or close button)."""
        while True:
            loop = self.main_menu()
            if not loop:
                break

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
            'message': 'Selected profile: {}',  # Placeholder for the profile name
            'choices': {'Start instalocker': self.start_instalocker_menu,
                        **no_profile_selected['choices']
                        }
        }

        # Define the options according to the criteria
        # Does not have a region.
        if not self.region:
            # Add empty choice to prevent easygui: "ValueError: at least two choices need to be specified"
            no_region['choices'][''] = lambda: None
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
                self.profile.name.title())
            info = has_profile_and_region

        # get the input from the user
        msg = info['message'] + '\n\nPick a option'
        available_choices = info['choices']
        user_choice: str | None = eg.choicebox(msg,
                                               'Main Menu',
                                               list(available_choices.keys()))  # type: ignore

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
            eg.msgbox(f'Region {self.region.upper()} selected successfully!',  # type: ignore
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
                    ph.dump_profile(ph.Profile(profile_name,
                                               game_mode,
                                               map_agent))
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
            self.profile = ph.load_profile(profile_name)
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
                ph.delete_profile(profile_name)
                self.profile = None
                eg.msgbox(f'Profile "{profile_name}" deleted Successfully',
                          'Profile deletion')
                return True
            else:
                eg.msgbox(f'Profile {profile_name} not deleted',
                          'Profile deletion')
        return False

    def start_instalocker_menu(self) -> bool:
        valorant_is_running = eg.ynbox('Make sure that valorant is running before start the instalocker.\nStart the instalocker before you start the matchmaking.',
                                        'Instalocker',
                                        ["[<F1>]Valorant is running. Start Instalocker", "[<F2>]Return to main menu"])
        if not valorant_is_running:
            return False   
        
        locker = instalocker.Instalocker(self.region, self.profile) # type: ignore
        success = locker.run()
        
        # TODO: finish testing the Instalocker to finish this menu
        if not success:
            print('not instalocked')
            return False
        
        print('instalocked')
        return True

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
    return [profile_file.removesuffix('.json') for profile_file in os.listdir(const.PROFILE_PATH)]


def get_region(msg: str) -> str | None:
    # sourcery skip: assign-if-exp, reintroduce-else
    """Get a region from the user.

    Args:
        msg (str): The message for the user.

    Returns:
        str | None: The chosen region or None if the user canceled the action. 
    """
    # Format regions to show all servers in the options
    options = []
    for acronym, places in const.REGIONS.items():
        opt = f'{acronym.upper()} - '
        for place_idx in range(len(places)):
            # Do not add the "," if it is the last item in the list
            opt += f'{places[place_idx]}, ' \
                if place_idx != len(places) - 1 \
                else places[place_idx]

        options.append(opt)

    choice: str | None = eg.choicebox(msg, 'Regions', options)  # type: ignore

    # User canceled operation
    if choice is None:
        return None

    # Get the unformatted acronym
    return choice.split('-')[0].strip().lower()


def get_game_mode(msg: str) -> ge.GameMode | None:
    """Get a game mode from the user.

    Args:
        msg (str): The message for the user

    Returns:
        ge.GameMode | None: The chosen game mode or None if the user canceled the action. 
    """
    # create and format options
    available_choices = [game_mode.name.replace('_', ' ').title()
                         for game_mode in ge.GameMode]
    choice: str | None = eg.choicebox(msg,
                                      'Game modes',
                                      available_choices)  # type: ignore

    # User canceled operation or the game mode
    return None if choice is None else ge.GameMode[choice.replace(' ', '_').upper()]


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
        agents_chosen: list[str] | None = eg.multenterbox(msg,
                                                          'Map-Agent selection',
                                                          maps_name)  # type: ignore
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
    user_input: list[str] | None = eg.multenterbox(msg,
                                                   title,
                                                   [''])  # type: ignore

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

    user_choice: str | None = eg.choicebox(msg,
                                           'Profile selection',
                                           profiles_name)  # type: ignore

    # Check if the user selected the empty string
    return None if (user_choice == '' or user_choice is None) else str(user_choice)


def main() -> int:
    app = Application(os.path.join(os.getcwd(), 'user_settings.txt'))
    app.run()
    return 0


if __name__ == '__main__':
    main()

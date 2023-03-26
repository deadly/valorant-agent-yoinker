# TODO: change selected set type and sets file format.
# TODO: maybe separate the functions in this file into different files
import easygui as eg
import os
import toml
import game_elements as ge
import instalocker

SETS_PATH = os.path.join(os.getcwd(), 'sets')

# selected_set type hint detailed: {name: set_name, game_mode: {map: agent}}
selected_set: dict = None
region: str = None


def main_menu() -> str | None:
    """Main menu with main options

    Returns:
        str | None: Str -> name of the option. None -> User canceled action 
    """
    global selected_set, region
    # Base choices. More choicer are added if the user match some criteria.
    choices = ['Region',
               'Quit']

    # Does not has a region.
    if not region:
        info = 'You haven\'n selected your region. Select a region to use Valorant instalocker'

    # Does not have any set created. Has region.
    elif not check_any_set_existence():
        info = 'You have no set created. Create a set to use Valorant instalocker'
        new_choices = ['Create new set']
        choices = new_choices + choices

    # Has at least one set created but none is selected. Has region.
    elif not selected_set:
        info = 'You have no set selected'
        new_choices = ['Select set',
                       'Delete set',
                       'Create new set']
        choices = new_choices + choices

    # Has a selected set. Has region.
    else:
        info = f'Selected set: {list(selected_set.values())[0]}\n'
        new_choices = ['Start instalocker',
                       'Select set',
                       'Delete set',
                       'Create new set']
        choices = new_choices + choices

    msg = info + '\n\nPick a option:'
    return eg.choicebox(msg, 'Main Menu', choices)


def select_set(set_name: str, set_content: dict[str, dict[str, str]]) -> None:
    """Define the "selected_set" global variable.
    If both args are None, the "selected_set" global variable becomes None.

    Args:
        set_name (str): The name of the set
        set_content (dict[str, dict[str, str]]): The set values
    """
    global selected_set

    # Remove the selected set if None is passed.
    # None is not a default value to prevention accidental deletion.
    if set_name is None and set_content is None:
        selected_set = None
        return
    selected_set = {'name': set_name, **set_content}


def delete_set(set_name: str) -> None:
    """Delete a set file

    Args:
        set_name (str): The name of the file without extension.
    """
    os.remove(f'{SETS_PATH}\\{set_name}.toml')


def get_game_mode(msg: str) -> ge.GameMode | None:
    """Get a game mode from the user

    Args:
        msg (str): The message that will appear on the screen

    Returns:
        ge.GameMode | None: ge.GameMode -> GameMode object. None -> User canceled action 
    """
    # Get formatted game mode names
    choices = [mode.name.replace('_', ' ').title() for mode in ge.GameMode]
    game_mode: str = eg.choicebox(msg, 'Game mode selection', choices)

    # Operation canceled
    if game_mode is None:
        return None

    # Fetch and return the GameMode object
    return ge.GameMode.__members__[game_mode.replace(' ', '_').upper()]


def get_map_agent(game_mode: ge.GameMode) -> dict[ge.Map, ge.Agent] | None:
    """User select one agent for each map

    Args:
        game_mode (ge.GameMode): The game mode name that will appear on the box message

    Returns:
        dict[ge.Map, ge.Agent] | None: dict -> Map and agent combination. None -> User canceled action 
    """
    maps_name = [game_map.name.title() for game_map in ge.Map]
    agents = [agent.name.title() for agent in ge.Agent]
    # Empty start to prevent "None is not iterable" error
    agents_name: list[str] = ['']

    # Infinity loop until user type valid names or cancel the operation
    valid = False
    while not valid:
        agents_name = eg.multenterbox(f'Type the character you like for each map in the {game_mode.name.title()} game mode',
                                      'Set Creation',
                                      maps_name)

        # Operation canceled
        if agents_name is None:
            return None

        # Validate agents
        for agent in agents_name:

            # Make sure that all maps have a agent
            if agent == "":
                eg.msgbox('Please, choose one agent for each map.',
                          'Set Creation')
                break

            # Check valid agent
            elif agent.title() not in agents:
                eg.msgbox(f'The agent {agent.title()} is not a valid agent.',
                          'Set Creation')
                break

            # Break the loop if everything is OK
            else:
                valid = True

    # Get object for each field
    agents_name = [ge.Agent.__members__[field.upper()]
                   for field in agents_name]

    # Return the dict with map and agent objects
    return dict(zip(list(ge.Map), agents_name))


def get_user_free_input(prompt: str, title: str, field_name: str) -> str:
    """Get a free input from the use

    Args:
        prompt (str): The message that will appear on the box
        title (str): The title of the box
        field_name (str): The name of the field where the user will input

    Returns:
        str: What the user inputted
    """
    user_input = eg.multenterbox(prompt, title, field_name)

    return None if user_input is None else user_input[0]


def create_set(set_name: str, game_mode: ge.GameMode, data: dict[ge.Map, ge.Agent]) -> None:
    """Create a set with the given data

    Args:
        set_name (str): The name of the set. No extension.
        game_mode (ge.GameMode): The game mode of the set
        data (dict[ge.Map, ge.Agent]): The map-agent combination

    Returns:
        bool: True if the set was created successfully, False otherwise.
    """
    # Format data
    game_mode = game_mode.name.replace('_', ' ').title()
    data = {k.name.title(): v.name.title() for k, v in data.items()}

    # Create the file
    with open(f'{SETS_PATH}\\{set_name}.toml', 'w')as f:
        toml.dump({game_mode: data}, f)


def get_set_name() -> str:
    """Get a existent set name of the user choice. Does not return the file extension, just the set name

    Returns:
        str: The set name
    """
    sets_names = [set_file.removesuffix('.toml')
                  for set_file in os.listdir(SETS_PATH)]

    # Add empty string to avoid "ValueError: at least two choices need to be specified".
    # This empty option is equivalent to clicking in cancel
    sets_names.append('')
    choice = eg.choicebox('Select the set you want',
                          'Set selection', sets_names)

    # Check if the user selected the empty string
    return None if choice == '' else choice


def get_set_content(set_name: str) -> dict[str, dict[str, str]] | None:
    """Return the content of a toml file (aka set in the project context)

    Args:
        set_name (str): The name of the set

    Returns:
        dict[str, dict[str, str]] | None: dict -> The set content. None -> Error reading the file
    """
    content = None
    try:
        with open(f'{SETS_PATH}\\{set_name}.toml', 'r')as f:
            content = toml.load(f)
        return content

    except FileExistsError:
        return None


def check_any_set_existence() -> bool:
    """Check there is at least one file in the set folder

    Returns:
        bool: True if there is at least one file. False if there is no files
    """
    return len(os.listdir(SETS_PATH)) != 0


def show_set_information(set_information: dict) -> None:
    """Show the set information.

    Args:
        set_information (dict): A set that is same type as the selected_set global variable
    """
    msg = f'Name: {list(set_information.values())[0]}\n\n'
    msg += f'Game mode: {list(set_information.keys())[1]}\n\n'

    for game_map, game_character in list(set_information.values())[1].items():
        msg += f'{game_map:<10}{game_character}\n'

    eg.msgbox(msg, list(set_information.values())[0])


def get_region() -> str | None:
    """Get the user region

    Returns:
        str | None: The region or None
    """

    # Define the regions and its equivalents
    regions = ["na", "eu", "latam", "br", "ap", "kr", "pbe"]

    choice = eg.choicebox('Select your region',
                          'Region selection',
                          regions)

    # User canceled operation or choice
    return None if choice is None else choice


def set_user_settings() -> None:
    global region, selected_set
    # format data
    l_region = region
    l_selected_set = selected_set

    if l_region is None:
        l_region = ""

    l_selected_set = "" if l_selected_set is None else list(
        l_selected_set.values())[0]

    with open(os.path.join(os.getcwd(), 'user_settings.toml'), 'w') as f:
        toml.dump({'region': l_region, 'selected_set': l_selected_set}, f)
    return None


def main() -> int:
    global selected_set, region

    # Try to restore previous settings
    with open(os.path.join(os.getcwd(), 'user_settings.toml'), 'r') as f:
        data = toml.load(f)
        if set_name := data["selected_set"]:
            selected_set = {'name': set_name, **get_set_content(set_name)}

        region = data["region"]

    while True:
        main_option = main_menu()

        match main_option:
            case "Start instalocker":
                if eg.ynbox('Make sure that valorant is running before start the instalocker.\n',
                            'Instalocker',
                            ["[<F1>]Valorant is running. Start Instalocker", "[<F2>]Return to main menu"]):
                    instalocker.instalocker(region, selected_set)

            case "Select set":
                if set_name := get_set_name():
                    content = get_set_content(set_name)
                    select_set(set_name, content)
                    set_user_settings()
                    show_set_information(selected_set)

            case "Delete set":
                if set_name := get_set_name():
                    if eg.ynbox(f'Delete the set {set_name}', 'Set Deletion'):
                        delete_set(set_name)
                        select_set(None, None)
                        set_user_settings()
                        eg.msgbox('Set deleted Successfully', 'Set deletion')
                    else:
                        eg.msgbox('Set not deleted', 'Set deletion')

            case "Create new set":
                msg = 'Choose your favorite game mode to create a set for it.'
                if game_mode := get_game_mode(msg):
                    if map_agent := get_map_agent(game_mode):
                        if set_name := get_user_free_input('How do you what to name your set?', 'Set name', ['']):
                            create_set(f'{set_name}', game_mode, map_agent)
                            eg.msgbox('Set created successfully!\nYou can select it from the "Select set" option',
                                      'Success')

            case "Region":
                if region_choice := get_region():
                    region = region_choice
                    eg.msgbox('Region selected successfully!', 'Success')
                    set_user_settings()

            case "Quit":
                break

            case _:
                break

    return 0


if __name__ == '__main__':
    main()

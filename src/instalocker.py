import multiprocessing as mp
import time

import easygui as eg
from valclient.client import Client, PhaseError

import game_elements as ge
import profile_handler as ph

# TODO: make this file naming consistent: (it includes doc-strings, comments and type hints)
# - sometimes "agent selection phase" is used, sometimes "match finding" is used, and sometimes "pre game" is used so reference the same thing.

# TODO: Make the class reusable. it includes:
# - setting the stop_flag variable to False after use;
# - cleaning the return_queue;
# - etc...


class Instalocker:
    def __init__(self, region: str, profile: ph.Profile) -> None:
        # Start the client
        self._client = Client(region)
        self._client.activate()

        self.profile: ph.Profile = profile

        self.timeout = 120
        self.delay = 2

        # Process related stuff
        self.stop_flag = mp.Value('b', False)
        self.return_queue = mp.Queue()

    def run(self) -> bool:
        """Runs the instalocker.

        Returns:
            bool: True if the a agent was successfully instalocked, False otherwise.
        """
        match_info = self.wait_agent_selection()
        print(match_info)

        # Check if the match was successfully found
        if not match_info:
            return False

        # Check the game mode
        if self.get_match_game_mode(match_info) != self.profile.game_mode:
            return False

        # Get the agent for the map
        agent = self.profile.map_agent[self.get_match_map(match_info)]

        # check if the user does not wants to instalock in this map
        if agent is None:
            return False

        # Instalock the character
        # TODO: check the return value of pregame_lock_character to know if the character was successfully instalocked and return True of False. For example what happens if someone already locked the character.
        lock_info = self._client.pregame_lock_character(agent.value)
        print(lock_info)
        print("\n\n")
        print(lock_info['Teams'][0]['Players'][0]['CharacterSelectionState'])
        if not lock_info:
            return False

        return True

    def wait_agent_selection(self) -> dict:
        """Waits for the agent selection phase and return the pre game match information.

        will wait until:
            - The agent selection phase starts. Return the match information
            - Timeout occur. Return a empty dict.
            - User cancel operation. Return a empty dict.

        This function handle two processes: One for finding the match and other to let the user cancel the math finding.

        Returns:
            dict: The match information or a empty dict.
        """
        # Create processes
        get_pregame_match_process = mp.Process(target=self._get_pregame_match,
                                               daemon=True)
        monitor_process = mp.Process(target=self._monitor,
                                     daemon=True)

        # Start both processes
        get_pregame_match_process.start()
        monitor_process.start()

        # Wait until the match process finish. It can happen due to:
        # - The agent selection phase starts
        # - Timeout occur
        # - User cancel operation (from the monitor process)
        get_pregame_match_process.join()
        if monitor_process.is_alive():
            # if monitor process is alive, it means that the user dit not cancel the match finding. So the msg box is still open.
            # Terminate the process to close the msg box.
            monitor_process.terminate()
            monitor_process.join()

        # return the result of the get_pregame_match process
        return self.return_queue.get()

    def _get_pregame_match(self) -> None:
        """Get the match information when the player enters the agent selection phase.

        Store the information on the return_queue.

        If this function reach its timeout, a empty dict will be returned.
        If the stop flag is set to True, this functions will return a empty dict.

        Returns:
            dict: The math information or an empty dict.
        """
        start_time = time.time()
        while True:
            # Check for timeout
            if (time.time() - start_time) >= self.timeout:
                self.return_queue.put({})
                return

            # Check for flag
            if self.stop_flag.value:  # type: ignore
                self.return_queue.put({})
                return

            try:
                # If pregame_fetch_match does not raise a error it means that the player is in a pre-game
                match_info = self._client.pregame_fetch_match()
                self.return_queue.put(match_info)
                return

            # Check for the PhaseError, that means the player is not in the pre-game yet.
            # If this error occur, we keep trying
            except PhaseError:
                # loop delay to reduce API calls
                time.sleep(self.delay)
                continue

    def _monitor(self) -> None:
        """Prompts the user to cancel the agent selection phase to start.

        If the user interacts with the box, the stop flag will be set to true and the match finding will stop.
        """
        eg.msgbox('The instalocker is waiting for the agent selection phase.',
                  'Instalocker',
                  ok_button='Stop Instalocker')

        # If the user never interact with the msgbox, the code will never reach here and the process will terminate and close the msgbox.
        self.stop_flag.value = True  # type: ignore

    def get_match_game_mode(self, match_info: dict) -> ge.GameMode:
        """Return a game mode object from the match information.

        Args:
            match_info (dict): Match information. The return of the valclient.client.Client.pregame_fetch_match()

        Returns:
            ge.GameMode: The game mode
        """
        game_mode = match_info['Mode'].split('/')[-2]
        # "QueueID" tells if the game is competitive.
        # If the game is NOT competitive, "QueueID" will be a empty string. Tus, not affecting "game_mode"
        # If the game IS competitive, "QueueID" will be "Competitive".
        return ge.GameMode(game_mode)

    def get_match_map(self, match_info: dict) -> ge.Map:
        """Return a map object from the match information.

        Args:
            match_info (dict): Match information. The return of the valclient.client.Client.pregame_fetch_match()

        Returns:
            ge.Map: The map
        """
        game_map = match_info['MapID'].split('/')[-2]
        return ge.Map(game_map)

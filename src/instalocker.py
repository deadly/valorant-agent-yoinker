import time

from valclient.client import Client, PhaseError

import game_elements as ge
import profile_handler as ph


class Instalocker:
    def __init__(self, region: str, profile: ph.Profile) -> None:
        self.profile: ph.Profile = profile
        
        # Start the client
        self.client = Client(region)
        self.client.activate()
        
        self.timeout = 120
        self.delay = 2
        # Flag to stop the match fetch before the timeout
        self.stop_instalocker = False
        
    def get_pregame_match(self) -> dict | None:
        """Returns the match information when the player enters the agent selection phase.
        
        This function has a timeout. If the function reach its timeout, None will be returned.
        This functions will also return None if the self.stop_instalocker flag is set to True.
        
        Returns:
            dict | None: The math information or None.
        """
        start_time = time.time()
        while True:
            # Check for timeout
            if (time.time() - start_time) >= self.timeout:
                return None
            
            # Check for flag
            if self.stop_instalocker:
                return None
                
            # loop delay to reduce API calls
            time.sleep(self.delay)

            try:
                # If pregame_fetch_match does not raise a error it means that the player is in a pre-game
                match_info = self.client.pregame_fetch_match()
                break
            
            # Check for the PhaseError, that means the player is not in the pre-game yet.
            # If this error occur, we keep trying
            except PhaseError:
                continue
                    
        return match_info
    
    def get_match_game_mode(self, match_info: dict) -> ge.GameMode:
        """Return a game mode object from the match information.

        Args:
            match_info (dict): Match information. The return of the valclient.client.Client.pregame_fetch_match()

        Returns:
            ge.GameMode: The game mode
        """
        # TODO: finish this function and use correct return
        game_mode = match_info['Mode']
        print(game_mode)

        return ge.GameMode.COMPETITIVE


    def get_match_map(self, match_info: dict) -> ge.Map:
        """Return a map object from the match information.

        Args:
            match_info (dict): Match information. The return of the valclient.client.Client.pregame_fetch_match()

        Returns:
            ge.Map: The map
        """
        # TODO: finish this function and use correct return
        game_map = match_info['MapID']  # .split('/')[-1].lower()
        print(game_map)

        return ge.Map.ASCENT


    def instalock(self) -> bool:
        # Try to get the pregame match information
        match_info = self.get_pregame_match()
        
        # If timeout
        if not match_info:
            return False
            
        # Check the game mode
        match_game_mode = self.get_match_game_mode(match_info)
        if match_game_mode == self.profile.game_mode:
            # Get the agent for the map
            agent = self.profile.map_agent[self.get_match_map(match_info)]

            # check if the user does not wants to instalock in this map
            if agent is None:
                return False

            # Instalock the character
            # TODO: check the return value of pregame_lock_character to know if the character was successfully instalocked and return True of False
            if self.client.pregame_lock_character(agent.value):
                return True
            
        return False
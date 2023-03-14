
class Player:
    def __init__(self, client):
        self.client = client
        self.puuid = self.client.puuid
        self.name = self.set_name(self.puuid)
        self.seenMatches = [] # array of match IDs
        self.currentMatch = None # contains ALL information about current match

    def set_name(self, puuid):
        playerData = self.client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[puuid]
        )[0]

        return f"{playerData['GameName']}#{playerData['TagLine']}"
    
    def hover_agent(self, agentID):
        self.client.pregame_select_character(agentID)
    
    def lock_agent(self, agentID):
        self.client.pregame_lock_character(agentID)
    
    def acknowledge_current_match(self):
        # append current match ID to seenMatches
        self.seenMatches.append(self.client.pregame_fetch_match()['ID'])
        # update currentMatch to the current pregame
        self.currentMatch = self.client.pregame_fetch_match()
    
    def get_side(self):
        teamID = self.currentMatch['Teams'][0]['TeamID']

        if (teamID == 'Blue'):
            return 'Defending'
        else:
            return 'Attacking'


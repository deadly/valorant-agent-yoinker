class Player:
    def __init__(self, client):
        self.client = client
        self.puuid = self.client.puuid
        self.name = self.set_name(self.puuid)
        self.seenMatches = [] # array of match IDs
        self.currentMatch = {'map': 'current map', 'ID': 'current ID'}

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
        matchInfo = self.client.pregame_fetch_match()
        self.seenMatches.append(matchInfo['ID'])
    
    def get_current_match(self):
        matchInfo = self.client.pregame_fetch_match()
        self.currentMatch['map'] = matchInfo['MapID']
        self.currentMatch['ID'] = matchInfo['ID']
        return self.currentMatch
    
    def get_seen_matches(self):
        return self.seenMatches

    def get_side(self):
        teamID = self.currentMatch['Teams'][0]['TeamID']

        if (teamID == 'Blue'):
            return 'Defending'
        else:
            return 'Attacking'


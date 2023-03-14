
class Player:
    def __init__(self, client):
        self.client = client
        self.puuid = self.client.puuid
        self.name = self.set_name(self.puuid)

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
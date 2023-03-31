import enum


class GameMode(enum.Enum):
    # check for "QueueID" to find if the "Bomb" game mode is competitive
    UNRATED = "Bomb"
    COMPETITIVE = "Bomb" + "Competitive"
    SWIFTPLAY = "Swiftplay_EndOfRoundCredits"
    REPLICATION = "OneForAll"
    SPIKE_RUSH = "QuickBomb"


class Map(enum.Enum):
    ASCENT = "Ascent"
    BIND = "Duality"
    BREEZE = "Foxtrot"
    FRACTURE = "Canyon"
    HAVEN = "Triad"
    ICEBOX = "Port"
    PEARL = "Pitt"
    SPLIT = "Bonsai"
    LOTUS = "Jam"


class Agent(enum.Enum):
    JETT = "add6443a-41bd-e414-f6ad-e58d267f4e95"
    REYNA = "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc"
    RAZE = "f94c3b30-42be-e959-889c-5aa313dba261"
    YORU = "7f94d92c-4234-0a36-9646-3a87eb8b5c89"
    PHOENIX = "eb93336a-449b-9c1b-0a54-a891f7921d69"
    NEON = "bb2a4828-46eb-8cd1-e765-15848195d751"
    BREACH = "5f8d3a7f-467b-97f3-062c-13acf203c006"
    SKYE = "6f2a04ca-43e0-be17-7f36-b3908627744d"
    SOVA = "320b2a48-4d9b-a075-30f1-1f93a9b638fa"
    KAYO = "601dbbe7-43ce-be57-2a40-4abd24953621"
    KILLJOY = "1e58de9c-4950-5125-93e9-a0aee9f98746"
    CYPHER = "117ed9e3-49f3-6512-3ccf-0cada7e3823b"
    SAGE = "569fdd95-4d10-43ab-ca70-79becc718b46"
    CHAMBER = "22697a3d-45bf-8dd7-4fec-84a9e28c69d7"
    OMEN = "8e253930-4c05-31dd-1b6c-968525494517"
    BRIMSTONE = "9f0d8ba9-4140-b941-57d3-a7ad57c6b417"
    ASTRA = "41fb69c1-4189-7b37-f117-bcaf1e96f1bf"
    VIPER = "707eab51-4836-f488-046a-cda6bf494859"
    FADE = "dade69b4-4f5a-8528-247b-219e5a1facd6"
    HARBOR = "95b78ed7-4637-86d9-7e41-71ba8c293152"
    GEKKO = "e370fa57-4757-3604-3648-499e1f642d3f"

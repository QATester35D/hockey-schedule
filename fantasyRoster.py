#  Slot, Position,  Player,     Team,  Status, PTS20232024,Line  (note: "PTS20232024" is points from the 2023-2024 season)
#"Starter","F","Connor McDavid","Edm","Healthy","250.9","1"
fantasyRosterTuple = [("Starter","F","Connor McDavid","Edm","Healthy","250.9","1"),
    ("Starter","F","Connor Bedard","Chi","Healthy","136.7","1"),
    ("Starter","F","Wyatt Johnston","Dal","Healthy","157","1"),
    ("Starter","F","Fabian Zetterlund","SJ","Healthy","148.9","1"),
    ("Starter","F","Trevor Moore","LA","Healthy","158.5","3"),
    ("Starter","F","Alexis Lafreniere","NYR","Healthy","127.7","1"),
    ("Starter","F","Mark Scheifele","Wpg","Healthy","152.9","1"),
    ("Starter","F","Tom Wilson","Wsh","Healthy","140.4","2"),
    ("Starter","F","Matty Beniers","Sea","Healthy","104.3","1"),
    ("Starter","D","Rasmus Dahlin","Buf","Healthy","212.9","1"),
    ("Starter","D","Josh Morrissey","Wpg","Healthy","169.7","1"),
    ("Starter","D","Jake Sanderson","Ott","Healthy","147.6","1"),
    ("Starter","D","Seth Jones","Chi","Healthy","136.3","1"),
    ("Starter","D","Travis Sanheim","Phi","Healthy","157","1"),
    ("UTIL","D","K'Andre Miller","NYR","Healthy","119.6","2"),
    ("Bench","F","Elias Lindholm","Bos","DTD","129","1"),
    ("Bench","F","Anthony Cirelli","TB","Healthy","130.2","2"),
    ("Bench","D","Jake Middleton","Min","Healthy","134.5","2"),
    ("Bench","D","Mason Lohrei","Bos","Healthy","58.1","3"),
    ("Starter","G","Connor Hellebuyck","Wpg","Healthy","214.2","1"),
    ("Starter","G","Frederik Andersen","Car","Healthy","81.4","2"),
    ("Bench","G","Logan Thompson","Wsh","Healthy","105.8","2")
]

#Similar methods as in proTeams.py so maybe inherit them?
#Uniqueness is that there can be multiple players with/on the same team
def findTeamInTuple (teamName):
    #If abbrev is mixed case, check for a length of 3 (3=abbrev), then make value all uppercase
    if len(teamName) == 3:
        teamName=teamName.upper()
    for sublist in fantasyRosterTuple:
        for element in sublist:
            if element == teamName:
                return sublist
    return None #if value not found

def findIndexOfTeamInTuple (teamName):
    if len(teamName) == 3:
        teamName=teamName.upper()
    for sublist in fantasyRosterTuple:
        for element in sublist:
            if element == teamName:
                teamIndex=fantasyRosterTuple.index(sublist)
                return teamIndex
    return None #if value not found
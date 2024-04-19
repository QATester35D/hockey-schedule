# A module to find a team by the abbrev or full name and return the tuple of info for use in the code
proTeamTuple = [("BOS","Boston Bruins","BOS.png"),
    ("BUF","Buffalo Sabres","BUF.png"),
    ("CGY","Calgary Flames","CGY.png"),
    ("CHI","Chicago Blackhawks","CHI.png"),
    ("DET","Detroit Red Wings","DET.png"),
    ("EDM","Edmonton Oilers","EDM.png"),
    ("CAR","Carolina Hurricanes","CAR.png"),
    ("LAK","Los Angeles Kings","LA.png"),
    ("DAL","Dallas Stars","DAL.png"),
    ("MTL","Montréal Canadiens","MTL.png"),
    ("NJD","New Jersey Devils","NJ.png"),
    ("NYI","New York Islanders","NYI.png"),
    ("NYR","New York Rangers","NYR.png"),
    ("OTT","Ottawa Senators","OTT.png"),
    ("PHI","Philadelphia Flyers","PHI.png"),
    ("PIT","Pittsburgh Penguins","PIT.png"),
    ("COL","Colorado Avalanche","COL.png"),
    ("SJS","San Jose Sharks","SJ.png"),
    ("STL","St. Louis Blues","STL.png"),
    ("TBL","Tampa Bay Lightning","TB.png"),
    ("TOR","Toronto Maple Leafs","TOR.png"),
    ("VAN","Vancouver Canucks","VAN.png"),
    ("WSH","Washington Capitals","WSH.png"),
    ("ARI","Arizona Coyotes","ARI.png"),
    ("ANA","Anaheim Ducks","ANA.png"),
    ("FLA","Florida Panthers","FLA.png"),
    ("NSH","Nashville Predators","NSH.png"),
    ("WPG","Winnipeg Jets","WPG.png"),
    ("CBJ","Columbus Blue Jackets","CBJ.png"),
    ("MIN","Minnesota Wild","MIN.png"),
    ("VGK","Vegas Golden Knights","VGK.png"),
    ("SEA","Seattle Kraken","SEA.png")
]

def findTeamRowInTuple (teamName):
    #If abbrev is mixed case, check for a length of 3 (3=abbrev), then make value all uppercase
    if len(teamName) == 3:
        teamName=teamName.upper()
    for sublist in proTeamTuple:
        for element in sublist:
            if element == teamName:
                return sublist
    return None #if value not found

def findIndexOfTeamInTuple (teamName):
    if len(teamName) == 3:
        teamName=teamName.upper()
    for sublist in proTeamTuple:
        for element in sublist:
            if element == teamName:
                teamIndex=proTeamTuple.index(sublist)
                return teamIndex
    return None #if value not found
    
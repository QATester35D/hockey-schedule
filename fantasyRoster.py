import time
#List of tuples
#  Slot, Position,  Player,     Team,  Status, PTS20232024,Line  (note: "PTS20232024" is points from the 2023-2024 season)
#"Starter","F","Connor McDavid","Edm","Healthy","250.9",    "1"
#    0      1         2           3       4         5        6
fantasyRosterTuple = [("Starter","F","Connor McDavid","EDM","Healthy","250.9","1"),
    ("Starter","F","Connor Bedard","CHI","Healthy","136.7","1"),
    ("Starter","F","Wyatt Johnston","DAL","Healthy","157","1"),
    ("Starter","F","Fabian Zetterlund","SJS","Healthy","148.9","1"),
    ("Starter","F","Trevor Moore","LAK","Healthy","158.5","3"),
    ("Starter","F","Alexis Lafreniere","NYR","Healthy","127.7","1"),
    ("Starter","F","Mark Scheifele","WPG","Healthy","152.9","1"),
    ("Starter","F","Tom Wilson","WSH","Healthy","140.4","2"),
    ("Starter","F","Matty Beniers","SEA","Healthy","104.3","1"),
    ("Starter","D","Rasmus Dahlin","BUF","Healthy","212.9","1"),
    ("Starter","D","Josh Morrissey","WPG","Healthy","169.7","1"),
    ("Starter","D","Jake Sanderson","OTT","Healthy","147.6","1"),
    ("Starter","D","Seth Jones","CHI","Healthy","136.3","1"),
    ("Starter","D","Travis Sanheim","PHI","Healthy","157","1"),
    ("UTIL","D","K'Andre Miller","NYR","Healthy","119.6","2"),
    ("Bench","F","Elias Lindholm","BOS","DTD","129","1"),
    ("Bench","F","Anthony Cirelli","TBL","Healthy","130.2","2"),
    ("Bench","D","Jake Middleton","MIN","Healthy","134.5","2"),
    ("Bench","D","Mason Lohrei","BOS","Healthy","58.1","3"),
    ("Starter","G","Connor Hellebuyck","WPG","Healthy","214.2","1"),
    ("Starter","G","Frederik Andersen","CAR","Healthy","81.4","2"),
    ("Bench","G","Logan Thompson","WSH","Healthy","105.8","2")
]

#Similar methods as in proTeams.py so maybe inherit them?
#Uniqueness is that there can be multiple players with/on the same team
def whatTeamsIHave ():
    teamList=[]
    counter=1
    for sublist in fantasyRosterTuple:
        team=sublist[3]
        if counter==1:
            teamList.append([team,1])
            counter+=1
        else:
            found=False
            for i in teamList:
                if sublist[3] == i[0]:
                    cntr=i[1]+1
                    i[1]=cntr
                    found=True
                    break

            if found != True:
                teamList.append([team,1])

    return teamList

# teamList=whatTeamsIHave()
# time.sleep(1)
import time
#List of tuples
#  Slot, Position,  Player,     Team
#"Starter","F","Connor McDavid","Edm"
#    0      1         2           3
fantasyRosterTuple = [("Starter","F","Connor McDavid","EDM"),
    ("Starter","F","Connor Bedard","CHI"),
    ("Starter","F","Johnny Beecher","BOS"),
    ("Starter","F","Fabian Zetterlund","SJS"),
    ("Starter","F","Nick Foligno","CHI"),
    ("Starter","F","John Tavares","TOR"),
    ("Starter","F","Mark Scheifele","WPG"),
    ("Starter","F","Tom Wilson","WSH"),
    ("Starter","F","Jakub Lauko","MIN"),
    ("Starter","D","Rasmus Dahlin","BUF"),
    ("Starter","D","Josh Morrissey","WPG"),
    ("Starter","D","Jake Sanderson","OTT"),
    ("Starter","D","Seth Jones","CHI"),
    ("Starter","D","Brenden Dillon","NJD"),
    ("UTIL","F","Nino Niederreiter","WPG"),
    ("Bench","F","Elias Lindholm","BOS"),
    ("Bench","F","Anthony Cirelli","TBL"),
    ("Bench","D","Jake Middleton","MIN"),
    ("Bench","D","Johnathan Kovacevic","NJD"),
    ("Starter","G","Connor Hellebuyck","WPG"),
    ("Starter","G","Frederik Andersen","CAR"),
    ("Bench","G","Logan Thompson","WSH")
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
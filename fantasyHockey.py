import requests
import json
# import os
# import sys
# import proTeams
# import teamGameCount
import fantasyRoster
import excelMethods
from operator import itemgetter
# from openpyxl import Workbook
# from openpyxl.styles import Font, Color, Alignment, Border, Side, PatternFill
# from openpyxl.drawing.image import Image as ExcelImage
# from datetime import datetime, timedelta, date
# from PIL import Image
import time

############################################################################
# In the process of refactoring some of the code that is shared
## Need to hit player API to retrieve player stats
############################################################################

#This class parses thru the API json and creates a text file of the info for the schedule
class GetGameSchedule:
    def __init__(self,weekDate):
        weekDateCall='https://api-web.nhle.com/v1/schedule/'+weekDate #Looks like: 'https://api-web.nhle.com/v1/schedule/2024-03-25'
        self.nhlApi=requests.get(weekDateCall)

    def getGameDayInfo(self):
        r=self.nhlApi
        gamesPerDay=[]
        if r.status_code != 200:
            print ("Problem connecting with NHL API")
            exit
        theJSON = json.loads(r.content)
        for i in theJSON["gameWeek"]:
            dateGameOfWeek = i["date"]
            dayAbbrev = i["dayAbbrev"]
            dayNumberOfGames = i["numberOfGames"] #games for the day
            for j in i["games"]:
                awayTeam=j["awayTeam"]["abbrev"]
                homeTeam=j["homeTeam"]["abbrev"]
                gamesPerDay.append([dateGameOfWeek,dayAbbrev,dayNumberOfGames,awayTeam,homeTeam])
        return gamesPerDay
    
    def myTeamsPlaying(self, teamList, gamesPerDay):
        #Loop on day for the number of games, check teams against my teamList, then player list fantasyRosterTuple, create a new list
        whosPlaying=[]
        prevDateOfGame=None
        forwardCounter=defenseCounter=goalieCounter=extraForward=extraDefenseman=extraGoalie=0 #max 9 forwards, 5 defensemen, 2 goalies, 1 utility
        allGoaliesPlaying=False
        gpdListSize=len(gamesPerDay)
        gpdCtr=0
        # for i in range(gpdListSize):
        for i in gamesPerDay:
            # anyTeamsOnThisDay=0
            teams=[]
            dateOfGame=gamesPerDay[gpdCtr][0]
            if gpdCtr != 0:
                if dateOfGame != prevDateOfGame:
                    prevDateOfGame=dateOfGame
                    forwardCounter=defenseCounter=goalieCounter=extraForward=extraDefenseman=extraGoalie=benchCounter=0 #max 9 forwards, 5 defensemen, 2 goalies, 1 utility
                    allGoaliesPlaying=False
            else:
                prevDateOfGame=dateOfGame

            dayOfGame=gamesPerDay[gpdCtr][1]
            nbrGamesPerDay=gamesPerDay[gpdCtr][2]
            awayTeamId=self.searchTeamList(gamesPerDay[gpdCtr][3],teamList) #see if I have a player on this team
            if awayTeamId != None:
                teams.append(awayTeamId) #add team position nbr in teamList if player on team
            homeTeamId=self.searchTeamList(gamesPerDay[gpdCtr][4],teamList) #see if I have a player on this team
            if homeTeamId != None:
                teams.append(homeTeamId) #add team position nbr in teamList if player on team
            teamsSize=len(teams)
            for j in range(teamsSize):
                team=teams[j] #grab the team position nbr
                nbrPlayersPerTeam=teamList[team][1] #grab the nbr of players I have on this team
                playerList=self.playerListPerTeam(team)
                for p in range(nbrPlayersPerTeam):
                    playerPosition=playerList[p][0]
                    playerName=playerList[p][1]
                    playerTeam=playerList[p][2]
                    match playerPosition:
                        case "F":
                            forwardCounter+=1
                            if forwardCounter <= 9:
                                positionSlot="F"+str(forwardCounter)
                            else:
                                extraForward+=1
                                benchCounter+=1
                                positionSlot="BE"+str(benchCounter)
                        case "D":
                            defenseCounter+=1
                            if defenseCounter <= 5:
                                positionSlot="D"+str(defenseCounter)
                            else:
                                extraDefenseman+=1
                                benchCounter+=1
                                positionSlot="BE"+str(benchCounter)
                        case "G":
                            goalieCounter+=1
                            if goalieCounter <= 2:
                                positionSlot="G"+str(goalieCounter)
                            else:
                                extraGoalie+=1
                                positionSlot="Goalie BE"+str(extraGoalie)
                        case _:
                            print("Problem with the data. Expected a player position but instead got:",playerPosition)
                    
                    # if utilityPositionNeeded < 1:
                    #     positionSlot="UTIL"
                    # else:
                    #     print ("Trying to fill Utility position with more than 1 skater. This is player:", playerName,"position:",playerPosition)

                    whosPlaying.append([dateOfGame,positionSlot,playerName,playerTeam])
            gpdCtr+=1
            # forwardCounter=defenseCounter=goalieCounter=utilityPositionNeeded=0 #max 9 forwards, 5 defensemen, 2 goalies, 1 utility
            # allGoaliesPlaying=False
        return whosPlaying

    def searchTeamList(self, team, teamList):
        teamListSize=len(teamList)
        for i in range(teamListSize):
            if team == teamList[i][0]:
                return i
        return None

    def playerListPerTeam(self, teamNbr):
        playerList=[]
        teamInfo=teamList[teamNbr]
        fantasyRosterTupleSize=len(fantasyRoster.fantasyRosterTuple)
        # for i in range(teamInfo[1]):
        ctr=0
        for j in range(fantasyRosterTupleSize):
            if fantasyRoster.fantasyRosterTuple[j][3] == teamInfo[0]:
                ctr+=1
                playerPosition=fantasyRoster.fantasyRosterTuple[j][1]
                playerName=fantasyRoster.fantasyRosterTuple[j][2]
                playerTeam=fantasyRoster.fantasyRosterTuple[j][3]
                playerList.append([playerPosition,playerName,playerTeam])
                if ctr == teamInfo[1]:
                    continue        
        return playerList
    
    def identifyUtilPlayers(self, sortedWhosPlayingList):
        slotCount=[]
        forwardCounter=defenseCounter=dateCounter=0 #get count of positions to determine if a utility slot is needed
        # tooManyForwards=tooManyDefensemen=False
        #### refactor this - simplify it using this List Comprehension
        result = [x for x in sortedWhosPlayingList if x[0] == '2024-10-22' and x[1][0:2] == "BE"]
        aa=0
        for p in sortedWhosPlayingList:
            if dateCounter == 0:
                processingDate=p[0]
            if processingDate == p[0]:
                dateCounter+=1
                playerSlot=p[1]
                result = [x for x in sortedWhosPlayingList if x[0] == processingDate and x[1] == "BE1"]
                aa=0
                # ####don't need to do this since the slot is numbered, just go after the max F and D (like F10 and D6)
                # match playerSlot[0]: #max 9 forwards, 5 defensemen, 1 utility
                #     case "F":
                #         forwardCounter+=1
                #     case "D":
                #         defenseCounter+=1
            else:
                if forwardCounter <= 9 and defenseCounter <=5:
                    print("UTIL slot not needed, no extra guys for date:",processingDate)
                    forwardCounter=defenseCounter=dateCounter=0
                    continue
                if forwardCounter > 9 and defenseCounter <=5:
                    if forwardCounter == 10:
                        #need to get F10 for the date I'm processing; should I create a temp list above?
                        playingDate = processingDate
                        playerSlot = "F10"
                        result = [x for x in sortedWhosPlayingList if x[0] == processingDate and x[1] == "F10"]
                        index=sortedWhosPlayingList[p][1] = "UTIL"
                        forwardCounter=defenseCounter=dateCounter=0
                        continue
                if defenseCounter > 5 and forwardCounter <=9:
                    if defenseCounter == 6:
                        sortedWhosPlayingList[p][1] = "UTIL"
                        forwardCounter=defenseCounter=dateCounter=0
                        continue
                if forwardCounter > 9 and defenseCounter > 5:
                    a=1
                    forwardCounter=defenseCounter=dateCounter=0
                    continue

#Retrieve Schedule of "Who's playing"
#Calling a class to parse thru the API json and creates a list of the game schedule by day for the week
# dateGameOfWeek,dayAbbrev,dayNumberOfGames,awayTeam,homeTeam
#      0            1             2            3         4
#  2024-04-08      Mon            2           PIT       TOR
#  2024-04-08      Mon            2           VGK       VAN
#  2024-04-09      Tue            13          CAR       BOS
dateForTheWeek='2024-10-21'
a=GetGameSchedule(dateForTheWeek)
gamesPerDay=a.getGameDayInfo()
teamList=fantasyRoster.whatTeamsIHave()
whosPlaying=a.myTeamsPlaying(teamList,gamesPerDay)
sortedWhosPlayingList=sorted(whosPlaying, key=itemgetter(0,1,3))
a.identifyUtilPlayers(sortedWhosPlayingList)
time.sleep(1)
#Calling a class to parse thru the API json and creates a text file of the info for the schedule
# filename = "c:\\Temp\\demoHockeySchedule.txt"
# a.getNhlGameInfo(filename)

#Calling a class to create the excel file with the scheduled data
xName="c:\\Temp\\hockeydemo.xlsx"
rowOneHeader = ["Abbrev","Team Logo","MON","TUE","WED","THU","FRI","SAT","SUN","Game Count"]
rowOneHeaderCount=len(rowOneHeader)
excelNhlSchedule=excelMethods.WriteNHLSchedule(xName)
excelNhlSchedule.set_row_height(1, 15)
excelNhlSchedule.set_column_width(1, 10, 12)  # Set columns A to H to width 10
excelNhlSchedule.set_column_width(10, 11, 15)
i=1
for a in range(rowOneHeaderCount):
    excelNhlSchedule.set_cell_font(1, i, bold=True, color='090DF8')  # Set font bold and blue color for cell A1
    excelNhlSchedule.set_cell_alignment(1, i, horizontal='center', vertical='center')  # Center align cell A1
    excelNhlSchedule.set_cell_border(1, i)  # Add thin border to cell A1
    excelNhlSchedule.set_cell_fill_color(1, i, color='EEF8A6')  # Set light yellow fill color for cell A1
    i+=1

dayOfWeekIndex=0
excelNhlSchedule.write_row_data(1, rowOneHeader)  # Write data to row 1
#Figure out game count per team for the week
#Read Player dictionary of players on my fantasy team
#Based on player dictionary, retrieve the player id from their team info
#Based on player teams, sort roster by position and "games to play per team"
#Further sort the player list by their playing line

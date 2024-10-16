import requests
import json
# import os
# import sys
# import proTeams
# import teamGameCount
import fantasyRoster
# from openpyxl import Workbook
# from openpyxl.styles import Font, Color, Alignment, Border, Side, PatternFill
# from openpyxl.drawing.image import Image as ExcelImage
# from datetime import datetime, timedelta, date
# from PIL import Image
import time

#Probably want to consider refactoring some of the code that is shared

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
        gpdListSize=len(gamesPerDay)
        forwardCounter=defenseCounter=goalieCounter=utilityPositionNeeded=0 #max 9 forwards, 5 defensemen, 2 goalies, 1 utility
        allGoaliesPlaying=False
        gpdCtr=0
        # for i in range(gpdListSize):
        for i in gamesPerDay:
            # anyTeamsOnThisDay=0
            teams=[]
            dateOfGame=gamesPerDay[gpdCtr][0]
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
                                utilityPositionNeeded+=1
                        case "D":
                            defenseCounter+=1
                            if defenseCounter <= 5:
                                positionSlot="D"+str(defenseCounter)
                            else:
                                utilityPositionNeeded+=1
                        case "G":
                            goalieCounter+=1
                            if goalieCounter <= 2:
                                positionSlot="G"+str(goalieCounter)
                            else:
                                allGoaliesPlaying=True
                        case _:
                            print("Problem with the data. Expected a player position but instead got:",playerPosition)
                    
                    if utilityPositionNeeded > 1:
                        print ("Houston we have a problem")

                    if allGoaliesPlaying:
                        print ("Houston we have a problem")

                    whosPlaying.append([positionSlot,gamesPerDay[gpdCtr][0],playerName,playerTeam])
            gpdCtr+=1
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

#Retrieve Schedule of "Who's playing"
#Calling a class to parse thru the API json and creates a list of the game schedule by day for the week
# dateGameOfWeek,dayAbbrev,dayNumberOfGames,awayTeam,homeTeam
#      0            1             2            3         4
#  2024-04-08      Mon            2           PIT       TOR
#  2024-04-08      Mon            2           VGK       VAN
#  2024-04-09      Tue            13          CAR       BOS
dateForTheWeek='2024-04-08'
a=GetGameSchedule(dateForTheWeek)
gamesPerDay=a.getGameDayInfo()
teamList=fantasyRoster.whatTeamsIHave()
whosPlaying=a.myTeamsPlaying(teamList,gamesPerDay)
time.sleep(1)
#Figure out game count per team for the week

#Read Player dictionary of players on my fantasy team

#Based on player dictionary, retrieve the player id from their team info

#Based on player teams, sort roster by position and "games to play per team"

#Further sort the player list by their playing line

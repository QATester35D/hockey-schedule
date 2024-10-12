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
        # gamesPerDay=[("MON"),
        #     ("TUE"),
        #     ("WED"),
        #     ("THU"),
        #     ("FRI"),
        #     ("SAT"),
        #     ("SUN")
        # ]
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

#Retrieve Schedule
#Calling a class to parse thru the API json and creates a list of the game schedule by day for the week
# dateGameOfWeek,dayAbbrev,dayNumberOfGames,awayTeam,homeTeam
#  2024-04-08      Mon            2           PIT       TOR
#  2024-04-08      Mon            2           VGK       VAN
#  2024-04-09      Tue            13          CAR       BOS
dateForTheWeek='2024-04-08'
a=GetGameSchedule(dateForTheWeek)
gamesPerDay=a.getGameDayInfo()
time.sleep(1)
#Figure out game count per team for the week

#Read Player dictionary of players on my fantasy team

#Based on player dictionary, retrieve the player id from their team info

#Based on player teams, sort roster by position and "games to play per team"

#Further sort the player list by their playing line

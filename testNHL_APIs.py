import requests
import json
import os
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, Border, Side, PatternFill
from openpyxl.drawing.image import Image
from datetime import datetime, timedelta, date

# from constants import proTeamArray

#A class to find a team by the abbrev or full name and return the tuple of info for use later
class ProTeams:
    def __init__(self):
        # self.proTeamInfo = {}
        self.proTeamArray = [("BOS","Boston Bruins","BOS.png"),
            ("BUF","Buffalo Sabres","BUF.png"),
            ("CGY","Calgary Flames","CGY.png"),
            ("CHI","Chicago Blackhawks","CHI.png"),
            ("DET","Detroit Red Wings","DET.png"),
            ("EDM","Edmonton Oilers","EDM.png"),
            ("CAR","Carolina Hurricanes","CAR.png"),
            ("LA","Los Angeles Kings","LA.png"),
            ("DAL","Dallas Stars","DAL.png"),
            ("MTL","Montréal Canadiens","MTL.png"),
            ("NJ","New Jersey Devils","NJ.png"),
            ("NYI","New York Islanders","NYI.png"),
            ("NYR","New York Rangers","NYR.png"),
            ("OTT","Ottawa Senators","OTT.png"),
            ("PHI","Philadelphia Flyers","PHI.png"),
            ("PIT","Pittsburgh Penguins","PIT.png"),
            ("COL","Colorado Avalanche","COL.png"),
            ("SJ","San Jose Sharks","SJ.png"),
            ("STL","St. Louis Blues","STL.png"),
            ("TB","Tampa Bay Lightning","TB.png"),
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

    def findTeamRowInArray (self, teamName):
        #If abbrev is mixed case, check for a length of 3 (3=abbrev), then make value all uppercase
        if len(teamName) == 3:
            teamName=teamName.upper()
        for sublist in self.proTeamArray:
            for element in sublist:
                if element == teamName:
                    return sublist
        return None #if value not found

#This class parses thru the API json and creates a text file of the info for the schedule
class GetNHLSchedule:
    def __init__(self,weekDate):
        weekDateCall='https://api-web.nhle.com/v1/schedule/'+weekDate #Looks like: 'https://api-web.nhle.com/v1/schedule/2024-03-25'
        self.nhlApi=requests.get(weekDateCall)

    def delete_file_if_exists(self, fname): #check for file, delete if exists to avoid duplicate schedules
        if os.path.exists(fname): # Check if the file exists
            os.remove(fname) # If it exists, delete the file
            print(f"File '{fname}' deleted.")
        else:
            print(f"File '{fname}' does not exist.")

    def getNhlGameInfo(self, fname):
        r=self.nhlApi
        print(r.status_code)
        if r.status_code != 200:
            print ("Problem connecting with NHL API")
            exit
        self.delete_file_if_exists(fname) #delete the file if it already exists so we don't append to it
        f = open(fname, "a")
        theJSON = json.loads(r.content)
        for i in theJSON["gameWeek"]:
            dateGameOfWeek = i["date"]
            dayAbbrev = i["dayAbbrev"]
            dayNumberOfGames = i["numberOfGames"]
            for aRow in i["games"]:
                awayTeamName = aRow["awayTeam"]["placeName"]["default"]
                awayTeamAbbrev = aRow["awayTeam"]["abbrev"]
                homeTeamName = aRow["homeTeam"]["placeName"]["default"]
                homeTeamAbbrev = aRow["homeTeam"]["abbrev"]
                gameInfo=dateGameOfWeek+","+dayAbbrev+","+str(dayNumberOfGames)+","+awayTeamAbbrev+","+homeTeamAbbrev+'\n'
                f.write(gameInfo)
        f.close()

#A class to create the excel file with the scheduled data
class WriteNHLSchedule:
    def __init__(self, xName):
        self.filename = xName
        self.workbook = Workbook()
        self.ws = self.workbook.active
        self.imageObj = Image()
        self.img = self.imageObj

    def set_row_height(self, row, height):
        self.ws.row_dimensions[row].height = height

    def set_column_width(self, column, width):
        self.ws.column_dimensions[column].width = width

    def set_cell_font(self, row, column, font_name='Arial', font_size=11, bold=False, color=None):
        cell = self.ws.cell(row=row, column=column)
        cell.font = Font(name=font_name, size=font_size, bold=bold, color=color)

    def set_cell_alignment(self, row, column, horizontal='center', vertical='center'):
        cell = self.ws.cell(row=row, column=column)
        cell.alignment = Alignment(horizontal=horizontal, vertical=vertical)

    def set_cell_border(self, row, column, border_style='thin'):
        cell = self.ws.cell(row=row, column=column)
        border = Border(left=Side(style=border_style), right=Side(style=border_style), 
                        top=Side(style=border_style), bottom=Side(style=border_style))
        cell.border = border

    def set_cell_fill_color(self, row, column, color='FFFFFF'):
        cell = self.ws.cell(row=row, column=column)
        fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
        cell.fill = fill

    def set_column_width(self, start_column, end_column, width):
        for col in range(start_column, end_column):
            self.ws.column_dimensions[self.ws.cell(row=1, column=col).column_letter].width = width

    def write_row_data(self, row, data):
        for i, value in enumerate(data, start=1):
            self.ws.cell(row=row, column=i, value=value)

    def write_column_data(self, row, column, value):
        self.ws.cell(row=row, column=column, value=value)

    def insert_team_logo(self, row, column, imageName):
        row=str(row)
        cellName=column+row
        # img = Image('reflorestasp.png')
        # img.anchor('A1')
        self.img.anchor(cellName)
        self.ws.add_image(imageName,cellName)

    def save_excel(self):
        self.workbook.save(self.filename)

    def updateExcelWithSchedule (self, fName):
        # Open the text file in read mode to process through the schedule list
        with open(fName, 'r') as file:
            line = file.readline() # Read the first line
            while line: # Continue reading lines until reaching end of file
                # Process the current line (e.g., print it)
                print(line.strip())  # .strip() removes trailing newline characters
                line = file.readline() # Read the next line

#######
#Beginning of main code
#Calling the class to find a team by the abbrev or full name and return the tuple of info
team=ProTeams()
# teamRowInfo=team.findTeamRowInArray("Minnesota Wild") #can use abbrev too, returns a tuple of the team values
teamRowInfo=team.findTeamRowInArray("Col") #can use abbrev too, returns a tuple of the team values
if teamRowInfo == None: #exit when no team was found; probably a typo
    print("No team was found, exiting program as there is nothing to process.")
    sys.exit()
teamAbbrevName=teamRowInfo[0]
teamFullName=teamRowInfo[1]
teamImageName=teamRowInfo[2]
print(f"The team info is:{teamRowInfo}")

#Calling a class to parse thru the API json and creates a text file of the info for the schedule
dateForTheWeek='2024-03-25'
a=GetNHLSchedule(dateForTheWeek)
filename = "c:\\Temp\\demoHockeySchedle.txt"
a.getNhlGameInfo(filename)

#Calling a class to create the excel file with the scheduled data
###this needs updating
xName="c:\\Temp\\hockeydemo.xlsx"
daysOfWeek = ["Abbrev","Team Logo","MON","TUE","WED","THU","FRI","SAT","SUN","Game Count"]
daysOfWeekCount=len(daysOfWeek)
loopPlusThree=daysOfWeekCount+3
excelNhlSchedule=WriteNHLSchedule(xName)
excelNhlSchedule.set_row_height(1, 15)
excelNhlSchedule.set_column_width(1, 10, 12)  # Set columns A to H to width 10
excelNhlSchedule.set_column_width(10, 11, 15)
loopRange=loopPlusThree+1
for i in range(loopRange):
    i+=1
    excelNhlSchedule.set_cell_font(1, i, bold=True, color='090DF8')  # Set font bold and red color for cell A1
    excelNhlSchedule.set_cell_alignment(1, i, horizontal='center', vertical='center')  # Center align cell A1
    excelNhlSchedule.set_cell_border(1, i)  # Add thin border to cell A1
    excelNhlSchedule.set_cell_fill_color(1, i, color='EEF8A6')  # Set light yellow fill color for cell A1
dayOfWeekIndex=0
excelNhlSchedule.write_row_data(1, daysOfWeek)  # Write data to row 1
 
#get each day (date) for the week, for the column header
daysForTheWeek=[]
for i in range(8):
    if i==0:
        daysForTheWeek=[dateForTheWeek]
    else:
        Begindate = date.fromisoformat(dateForTheWeek)
        incremented_date = Begindate + timedelta(days=i)
        daysForTheWeek.append(incremented_date)
        print(daysForTheWeek[i])
dateHeader=[" "," ",daysForTheWeek[0],daysForTheWeek[1],daysForTheWeek[2],daysForTheWeek[3],daysForTheWeek[4],daysForTheWeek[5],daysForTheWeek[6],""]
excelNhlSchedule.write_row_data(2, dateHeader)

imagePath="C:\\Temp\\HockeyTeamLogos\\"
row=4
for i, value in enumerate(team.proTeamArray, start=00):
    excelNhlSchedule.set_row_height(row, 32)
    excelNhlSchedule.write_column_data(row, 1, value[0])
    imageName=imagePath+value[2]
    excelNhlSchedule.insert_team_logo(row, "B", imageName)
    row+=1

#Start writing text file scheduled contents
# f = open(filename, "rt") #r = read, t = text mode, but this really isn't needed since these are the defaults
# for x in f:
#     game=f.readline()
#     for g in range(game[2]):
#         excelNhlSchedule.write_row_data(3, daysOfWeek)
# f.close()

# excelNhlSchedule.workbook.close()
excelNhlSchedule.save_excel()
print("a")

########################################################
########################################################
#Old/original code follows - may use
def createInitialExcelSetup():
    #One time setup - Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook("c:\\Temp\\hockeydemo.xlsx")
    worksheet = workbook.add_worksheet()
    cell_format = workbook.add_format({"bold": True}) # Add a bold format to use to highlight cells.
    worksheet.set_column(0, 9, 20, cell_format) # 9 columns - Widen each column to make the text clearer.
    daysOfWeek = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    daysOfWeekCount=len(daysOfWeek)
    loopPlusTwo=daysOfWeekCount+2
    dayOfWeekIndex=0
    for a in range(loopPlusTwo): #for row 0 (first row)
        match a:
            case 0:
                worksheet.write(0, a, "Team Info") 
            case a if a in range(1,8):
                worksheet.write(0, a, daysOfWeek[dayOfWeekIndex])
                dayOfWeekIndex+=1
            case 8:
                worksheet.write(0, a, "Game Count")
    for a in range(loopPlusTwo): #for row 1 (second row)
        match a:
            case 0:
                worksheet.write(1, a, "Team Name") 
            case a if a in range(1,8):
                worksheet.write(1, a, daysOfWeek[dayOfWeekIndex])
                dayOfWeekIndex+=1
            case 8:
                worksheet.write(1, a, "Games For Week")
    for a in range(loopPlusTwo):
        match a:
            case 0:
                worksheet.write(2, a, "Team Name") 
            case a if a in range(1,8):
                worksheet.write(2, a, daysOfWeek[dayOfWeekIndex])
                dayOfWeekIndex+=1
            case 8:
                worksheet.write(2, a, "Games For Week")
    workbook.close()
    return

worksheetObject=createInitialExcelSetup()

# Use the json module to load the string data into a dictionary
r = requests.get('https://api-web.nhle.com/v1/schedule/2024-03-25')
print(r.status_code)
theJSON = json.loads(r.content)
# nbrOfGames = theJSON["gameWeek"][0] #this works, saving for later
for i in theJSON["gameWeek"]:
    dateGameOfWeek = i["date"]
    dayAbbrev = i["dayAbbrev"]
    dayNumberOfGames = i["numberOfGames"]
    for j in i["games"]:
        awayTeamName = j["awayTeam"]["placeName"]["default"]
        awayTeamAbbrev = j["awayTeam"]["abbrev"]
        homeTeamName = j["homeTeam"]["placeName"]["default"]
        homeTeamAbbrev = j["homeTeam"]["abbrev"]
        print("Away Team is",awayTeamName,"and the Home Team is",homeTeamName)

worksheet.write("A1", "Away Team") # Write some simple text.
worksheet.write("A2", awayTeamName, bold) # Text with formatting.
worksheet.set_row(1, 15) # Set row height
worksheet.insert_image("A3", "C:\\Temp\\HockeyTeamLogos\\STL.png") # Insert an image.
worksheet.set_row(2, 40)

worksheet.set_column("A:A", 20) # Widen the first column to make the text clearer.
worksheet.write("B1", "Home Team") # Write some simple text.
worksheet.write("B2", homeTeamName, bold) # Text with formatting.
worksheet.insert_image("B3", "C:\\Temp\\HockeyTeamLogos\\VGK.png") # Insert an image.

workbook.close()

#Figure out how to append to an existing file. Reopen it, append data and close
#Then make classes with inheritance to write the different data out using the child class with different methods
#
#Figure out how to put the array in a separate initialization file


# def main():
#     # define a variable to hold the source URL
    
#     urlData = "https://api-web.nhle.com/v1/club-schedule/NJD/week/2024-03-18"

#     # Open the URL and read the data
#     webUrl = requests.URLRequired(urlData)
#     # webUrl = urllib.request.urlopen(urlData)
#     print ("result code: " + str(webUrl.getcode()))
#     if (webUrl.getcode() == 200):
#         data = webUrl.read()
#         printResults(data)
#     else:
#         print("Received an error from the server, cannot print results", webUrl.getcode())

# if __name__ == "__main__":
#     main()
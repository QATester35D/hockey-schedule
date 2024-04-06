import requests
import json
import xlsxwriter
# from io import BytesIO
# from urllib.request import urlopen
# import cairosvg
# Import svglib and reportlab
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPM
class ProTeams:
    def __init__(self):
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
        for sublist in self.proTeamArray:
            for element in sublist:
                if element == teamName:
                    return sublist
        return None #if value not found

team=ProTeams()
teamRowInfo=team.findTeamRowInArray("COL") #returns the index for the value in the array (array starts with 0)
teamAbbrevName=teamRowInfo[0]
teamFullName=teamRowInfo[1]
teamImageName=teamRowInfo[2]
print(f"The team info is:{teamRowInfo}")

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
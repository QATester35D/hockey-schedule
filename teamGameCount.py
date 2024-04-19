#Create a dictionary that will keep track of a team's game count for the week
# class TeamGameCount:
# def __init__(self):
#     self.
teamListCount = {
    "BOS": 0,
    "BUF": 0,
    "CGY": 0,
    "CHI": 0,
    "DET": 0,
    "EDM": 0,
    "CAR": 0,
    "LAK": 0,
    "DAL": 0,
    "MTL": 0,
    "NJD": 0,
    "NYI": 0,
    "NYR": 0,
    "OTT": 0,
    "PHI": 0,
    "PIT": 0,
    "COL": 0,
    "SJS": 0,
    "STL": 0,
    "TBL": 0,
    "TOR": 0,
    "VAN": 0,
    "WSH": 0,
    "ARI": 0,
    "ANA": 0,
    "FLA": 0,
    "NSH": 0,
    "WPG": 0,
    "CBJ": 0,
    "MIN": 0,
    "VGK": 0,
    "SEA": 0
}

def teamGameCountIncrement(key):
    if key in teamListCount:
        teamListCount[key] += 1
    else:
        print(f"Key '{key}' not found.")

def teamGameCountRetrieval(key):
    return teamListCount.get(key)
    
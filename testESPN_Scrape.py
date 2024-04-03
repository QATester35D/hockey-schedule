# from espn_api.hockey import League
# league = League(league_id: int, year: int, espn_s2: str = None, swid: str = None, debug=False)

# league_id: int
# year: int
# settings: Settings
# teams: List[Team]
# draft: List[Pick]
# current_week: int # current fantasy football week
# nfl_week: int # current nfl week
# previousSeasons: List[str] # list of leagues previous seasons

import requests
from bs4 import BeautifulSoup

def scrape_espn_fantasy_hockey(url):
    # Send a GET request to the ESPN fantasy hockey webpage
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the section containing player rankings
        # rankings_section = soup.find('section', class_='PlayerTableTable')
        
        # Find all rows in the rankings table
        test1 = soup.find('class="jsx-1811044066 player-column__bio"')
        rows = soup.find_all('title')
        
        # Iterate over each row and extract player information
        for row in rows:
            # Find player name
            player_name = row.find('title', class_="jsx-1811044066 player-column__athlete flex")
            
            # Find player position
            player_position = row.find('td', class_='Table__TD').text
            
            # Find player team
            player_team = row.find('span', class_='hide-mobile').text
            
            # Find player ranking
            player_rank = row.find('td', class_='Table__TD').text
            
            # Print player information
            print(f"Name: {player_name}, Position: {player_position}, Team: {player_team}, Rank: {player_rank}")
    else:
        print("Failed to retrieve data from ESPN")

# URL of the ESPN fantasy hockey rankings page
url = 'https://fantasy.espn.com/hockey/players/add?leagueId=1074829076'
scrape_espn_fantasy_hockey(url)


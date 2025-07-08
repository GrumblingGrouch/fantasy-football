import requests
import json
import pyodbc

from importDataFunctions import *

league_id = 61893
years = [2024]#[2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,2020, 2021, 2022, 2023, 2024] 
views = ['kona_player_info']#['mPendingTransactions', 'mMatchup', 'mTeam', 'mBoxscore', 'mSettings', 'kona_player_info', 'player_wl', 'mSchedule', 'mMatchupScore']

cookies = {
    "swid": "{2AF4F7AC-6229-4198-B485-266CAF139DB2}",
    "espn_s2": "AEAe2f2C8mVaW5NBGsz%2FK75iCoNQ3pFeIl15tRCH8JSrIyRfpU7HiQ5lnC1dn1VHZd6rp5xtuTWQFNw16o%2BKgi2iog0KLY%2B8ReYRlwx5ZtEkHQLJPqgSf4wXLrX9iLJ69C58KUV9CQwPR4uTY41NhjigdHDziSVFH6PayhGdufUT8rUKjhFAjn1EbxiA9gTLxqLya%2FUcEO9b3K5WqlGkbV6uQTlGWibbcN8C6kOUi3nRgzVL8GXE093RGWtQZm0GvTH%2FnCXzAKQBERjJMls40gL%2BCIPkCfayhLTaDo1eS%2Bpk5w%3D%3D"
}

filters = {"players":{"filterStatus":{"value":["FREEAGENT","WAIVERS"]}}}
headers = {'x-fantasy-filter': json.dumps(filters)}


for year in years:
    print("Starting data load for league season year " + str(year))
    for view in views:  
        if year == 2024:
            url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id)
            if view == 'kona_player_info':
                r = requests.get(url, params={"view": view}, cookies=cookies, headers=headers)
            else:
                 r = requests.get(url, params={"view": view}, cookies=cookies)
            data = r.json()
        else: 
            url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(year)
            r = requests.get(url, params={"view": view})
            data = r.json()[0]
		
        print ("Start data import for view " + str(view))
        #Call appropriate fucniton depending on the view being translated to the DB.
        if view == 'mTeam':
            import_TeamsData(year, data)
        elif view == 'mMatchupScore':
            import_MatchupsData(year, data)
        elif view == 'kona_player_info':
            playerListFile(year, data)


import requests
import gspread
import json
from constant import *
from google.oauth2.service_account import Credentials

# === SETUP ===
SHEET_NAME = "The League DraftBoard 2025"
PLAYERDB_TAB = "PlayerDB"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "ff-the-palmetto-league-e69c8274c321.json"  # <-- Your service account credentials file

cookies = {
    "swid": "{2AF4F7AC-6229-4198-B485-266CAF139DB2}",
    "espn_s2": "AEAe2f2C8mVaW5NBGsz%2FK75iCoNQ3pFeIl15tRCH8JSrIyRfpU7HiQ5lnC1dn1VHZd6rp5xtuTWQFNw16o%2BKgi2iog0KLY%2B8ReYRlwx5ZtEkHQLJPqgSf4wXLrX9iLJ69C58KUV9CQwPR4uTY41NhjigdHDziSVFH6PayhGdufUT8rUKjhFAjn1EbxiA9gTLxqLya%2FUcEO9b3K5WqlGkbV6uQTlGWibbcN8C6kOUi3nRgzVL8GXE093RGWtQZm0GvTH%2FnCXzAKQBERjJMls40gL%2BCIPkCfayhLTaDo1eS%2Bpk5w%3D%3D"
}

# === Fetch player data from ESPN ===
#url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/" + str(year) + "/segments/0/leagues/" + str(league_id)

def fetch_espn_players():
    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2025/segments/0/leagues/61893?view=players_wl&limit=1000"
    filters = {"players":{"filterStatus":{"value":["FREEAGENT","WAIVERS"]}}}
    headers = {'x-fantasy-filter': json.dumps(filters)}

    response = requests.get(url, cookies=cookies, headers=headers)

    print("Status code:", response.status_code)
    print("Raw response text (first 300 chars):\n", response.text[:300])  # inspect what we got back

    if response.status_code != 200:
        raise Exception(f"ESPN API error {response.status_code}: {response.text}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception("Failed to parse JSON from ESPN: " + str(e))

    #write data to file 
    #file = open("FantasyJSONData/2025PlayerList.txt", "w")
    #file.write(json.dumps(data, indent=4))
    #file.close()


    players = data.get('players', [])

    filtered = []
    for player in players:
        p = player.get('player', {})
        pos_id = p.get("defaultPositionId")
        team_id = p.get("proTeamId")
        name = p.get("fullName")

        if pos_id in POSITION_MAP:
            filtered.append([
                name,
                POSITION_MAP[pos_id],
                PRO_TEAM_MAP.get(team_id, "UNK")
            ])
    return filtered


# === Push to Google Sheets ===
def push_to_sheets(data):
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    sheet = client.open(SHEET_NAME)
    ws = sheet.worksheet(PLAYERDB_TAB)

    # Clear existing data
    ws.clear()

    # Add header
    ws.append_row(["PlayerName", "Position", "Team"])

    # Append data
    ws.append_rows(data)

    print(f"Pushed {len(data)} players to PlayerDB")

# === Main execution ===
if __name__ == "__main__":
    players = fetch_espn_players()
    push_to_sheets(players)

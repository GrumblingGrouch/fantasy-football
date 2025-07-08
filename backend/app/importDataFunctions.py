####data function calls to write league data to the database.

import pyodbc
from constant import *
# Connection string to SQL Server
conn_str = (r'Driver=SQL Server;Server=OSCARDESKTOP\SQLEXPRESS;Database=TheLeague;Trusted_Connection=yes;'
# r'DRIVER={SQL Server};'
#r'SERVER=your_server;'
#r'DATABASE=your_database;'
#r'UID=your_username;'
#r'PWD=your_password;'
)



def import_TeamsData(year , data):

    #create DB connection
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    members = data.get('members', [])
    #loop through each member and insert into the table.
    for member in members:
        cursor.execute(
            "INSERT INTO leagueOwners (leagueSeasonYear, OwnerId, firstName, lastName) "
            "VALUES (?, ?, ?, ?) "
        , (year, member.get('id'), member.get('firstName'), member.get('lastName')))
        print("Member record inserted for " + str(year) + " and " +str(member.get('firstName')))

            
    #get teams data
    teams = data.get('teams', [])
    #loop through each team to get data and pull in info
    for team in teams:
        overall_record = team.get('record', {}).get('overall', {})
        transactionCounter = team.get('transactionCounter', {})
        cursor.execute(
            "INSERT INTO leagueTeams (leagueSeasonYear, teamId, teamName, teamOwnerId, wins, losses, ties, finalRank, pointsFor, pointsAgainst, faabSpent, waiverAcquisitions, waiverDrops, trades) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        , (year, team.get('id'), team.get('name'), team.get('primaryOwner'), overall_record.get('wins'), overall_record.get('losses'), overall_record.get('ties'), team.get('rankCalculatedFinal'), overall_record.get('pointsFor'), 
        overall_record.get('pointsAgainst'), transactionCounter.get('acquisitionBudgetSpent'), transactionCounter.get('acquisitions'), transactionCounter.get('drops'), transactionCounter.get('trades')))      
        print("Team record inserted for " + str(year) + " and " +str(team.get('name')))

    # Commit changes and close the connection
    conn.commit()
    conn.close()      
            
            
def import_MatchupsData(year, data):
    #create DB connection
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    matchups = data.get('schedule', [])
    
    #loop through each matchup
    for matchup in matchups:
        awayTeam = matchup.get('away', {})
        homeTeam = matchup.get('home', {})
        cursor.execute(
            "INSERT INTO leagueMatchups( leagueSeasonYear, matchupPeriodId, matchupId, playoffTierType, homeTeamId, homeTeamTotalScore, awayTeamId, awayTeamTotalScore, matchupWinner)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
        , (year, matchup.get('matchupPeriodId'), matchup.get('id'), matchup.get('playoffTierType'), homeTeam.get('teamId'), homeTeam.get('totalPoints'), awayTeam.get('teamId'), awayTeam.get('totalPoints'), matchup.get('winner')))
        
        print("Matchup record inserted for " + str(year) + ", matchup period " +str(matchup.get('matchupPeriodID')) + ", and matchup ID " + str(matchup.get('id')))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()      

def playerListFile(year, data):
    #Get player list
    players = data.get('players', [])
    
    #create file for data and open it
    file = open("C:/Users/orive/OneDrive/Desktop/PythonProjects/FantasyFootball/FantasyJSONData/" + str(year) + "/"  + "PlayerList.csv", "w")
        
    #loop through each player to get name position and team
    for player in players:
        p = player.get('player', {})
        
        #Set player Position
        playerPos = p.get('defaultPositionId')
        if playerPos == 1:
            playerPos = 'QB'
        elif playerPos == 2:
            playerPos = 'RB'
        elif playerPos == 3:
            playerPos = 'WR'
        elif playerPos == 4:
            playerPos = 'TE'                  
        elif playerPos == 16:
            playerPos = 'D/ST'
        
        #Get pro team from constants file
        proTeam = PRO_TEAM_MAP[p.get('proTeamId')]
        
        #write to file
        file.write(p.get('fullName') + "," + playerPos + "," + proTeam+"\n")
    file.close()

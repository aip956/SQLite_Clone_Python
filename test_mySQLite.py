from mySQLite import MySqliteRequest

# Selecting all players from nba_players.csv
request = MySqliteRequest().from_table('nba_players.csv').select('*')
print("All NBA Players:", request.run())

# Selecting a specific column (e.g. "name")
request = MySqliteRequest().from_table('nba_players.csv').select('name')
print("All NBA Player Names:", request.run())

# Filt
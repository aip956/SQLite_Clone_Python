from mySQLite import MySqliteRequest
import csv

# with open("nba_players.csv", "r", newline="") as file:
#     reader = csv.reader(file)
#     headers = next(reader) # Read the first row as header
#     print("CSV Headers:", headers)
 



# # Selecting all players from nba_players.csv
# request = MySqliteRequest().from_table('nba_players.csv').select('*')
# print("All NBA Players:", request.run())

# # Selecting a specific column (e.g. "name")
# request = MySqliteRequest().from_table('nba_players.csv').select('Player')
# print("All NBA Player Names:", request.run())

# Where condition test
print("\n SELECT Player WHERE birth_state = 'Indiana'")
request = MySqliteRequest().from_table("nba_players.csv").select(["Player", "birth_state"]).where("birth_state", "Indiana")
print(request.run())




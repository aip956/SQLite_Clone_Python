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
# print("\n SELECT Player WHERE birth_state = 'Indiana'")
# request = MySqliteRequest().from_table("nba_players.csv").select(["Player", "birth_state"]).where("birth_state", "Indiana")
# print(request.run())


# ORDER BY Test
print("\n SELECT Player ORDER BY height DESC")
request = MySqliteRequest().from_table("nba_players.csv").select(["Player", "height"]).order("DESC","height")
print(request.run())

# INSERT Test
print("\n INSERT INTO nba_players.csv")
new_player = {
    "Player": "Test Player",
    "height": "170",
    "weight": "90",
    "collage": "Test University",
    "born": "2000",
    "birth_city": "Test City",
    "birth_state": "Test State"
}
request = MySqliteRequest().insert("nba_players.csv").values(new_player)
print(request.run()) # Should print inserted row


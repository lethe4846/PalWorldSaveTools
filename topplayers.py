import csv
import re

# Define the path to the logfile
logfile_path = 'fix_save.log'
output_csv_path = 'players_data.csv'

# Function to extract player data from a line
def extract_player_data(line):
    pattern = r"Player: (.+?) \| UID: (.+?) \| Level: (\d+) \| Caught: (\d+) \| Owned: (\d+)"
    match = re.search(pattern, line)
    if match:
        player_name = match.group(1)
        pals_caught = int(match.group(4))
        return (player_name, pals_caught)
    return None

# List to hold all player data
players_data = []

# Read the logfile and extract data
with open(logfile_path, 'r', encoding='utf-8') as file:
    for line in file:
        data = extract_player_data(line)
        if data:
            players_data.append(data)

# Sort the list by Pals Caught in descending order
players_data.sort(key=lambda x: x[1], reverse=True)

# Write the sorted data to a CSV file using UTF-8 encoding
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Player', 'Pals Caught'])  # Writing the header
    for player in players_data:
        writer.writerow(player)

print('CSV file has been created and sorted by Pals Caught.')

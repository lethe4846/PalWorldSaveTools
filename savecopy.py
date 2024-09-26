import os
import time
from shutil import copy2, copytree
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the backup location from the environment variable
backup_location = os.getenv('SAVE_BACKUP_LOCATION')

# Function to find the most recently modified folder
def find_recent_folder(path):
    folders = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    recent_folder = max(folders, key=os.path.getmtime)
    return recent_folder

# Function to delete all files in the Players folder
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Continuously check the most recently modified folder until level.sav is found
while True:
    recent_folder = find_recent_folder(backup_location)
    level_save_path = os.path.join(recent_folder, 'level.sav')
    players_folder_path = os.path.join(recent_folder, 'Players')  # Path to the Players folder
    if os.path.exists(level_save_path):
        # Define the destination paths
        dest_level_save_path = 'Level.sav'
        dest_players_folder_path = './Players'  # Destination in the current working directory

        # Clear the Players directory before copying new files
        clear_directory(dest_players_folder_path)

        # Copy the file
        copy2(level_save_path, dest_level_save_path)
        # Copy the Players folder
        if os.path.exists(players_folder_path):
            copytree(players_folder_path, dest_players_folder_path, dirs_exist_ok=True)
            print(f'Copied Players folder from {recent_folder} to {dest_players_folder_path}')
        print(f'Copied level.sav from {recent_folder} to {dest_level_save_path}')
        break
    else:
        print(f'level.sav not found in {recent_folder}. Checking again in 5 seconds.')
        time.sleep(5)  # Wait for 5 seconds before checking again

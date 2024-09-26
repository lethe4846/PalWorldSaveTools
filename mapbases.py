import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
from datetime import datetime  # Import datetime

# Load the image
image_path = 'worldmap.png'
image = plt.imread(image_path)

# Define the grid boundaries
x_min, x_max = -1000, 1000
y_min, y_max = -1000, 1000

# Calculate the scaling factors to convert image coordinates to world coordinates
height, width = image.shape[:2]
x_scale = width / (x_max - x_min)
y_scale = height / (y_max - y_min)

# Function to convert world coordinates to image coordinates
def to_image_coordinates(x_world, y_world):
    x_img = (x_world - x_min) * x_scale
    y_img = (y_max - y_world) * y_scale  # y-axis is inverted in image coordinates
    return int(x_img), int(y_img)

# Read the CSV file for bases
df = pd.read_csv('bases.csv')

# Read the CSV for players
players_df = pd.read_csv('players_data.csv').head(20)

# Create string of top 20 players
top_players_text = "\n".join([f"{player['Player']} - {player['Pals Caught']}" for index, player in players_df.iterrows()])

# Parse totals from fix_save.log
totals = {}
with open('fix_save.log', 'r', encoding='utf-8') as file:
    for line in file:
        if 'Total Overall Pals:' in line:
            totals['Overall Pals'] = line.split(':')[-1].strip()
        elif 'Total Owned Pals:' in line:
            totals['Owned Pals'] = line.split(':')[-1].strip()
        elif 'Total Worker/Dropped Pals:' in line:
            totals['Worker Pals'] = line.split(':')[-1].strip()
        elif 'Total Active Guilds:' in line:
            totals['Guilds'] = line.split(':')[-1].strip()
        elif 'Total Bases:' in line:
            totals['Bases'] = line.split(':')[-1].strip()

# Plot the image with a specified resolution
fig, ax = plt.subplots(figsize=(81.92, 81.92), dpi=100)  # Adjust figure size to match the DPI to achieve 8192x8192 output
ax.imshow(image, aspect='equal')  # Ensure the image is not stretched

# Define red color
red_color = '#FF0000'

# Loop through the DataFrame and draw circles and text
for index, row in df.iterrows():
    for col in ['Base 1', 'Base 2', 'Base 3', 'Base 4']:
        if pd.notna(row[col]):
            x, y = map(int, row[col].split(', '))
            x_img, y_img = to_image_coordinates(x, y)
            # Draw a circle and text
            ax.add_patch(patches.Circle((x_img, y_img), 35, linewidth=3, edgecolor=red_color, facecolor='none'))
            text = ax.text(x_img, y_img + 70, row['Guild Leader'], color=red_color, ha='center', fontsize=25, weight='bold')
            text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='white'), path_effects.Normal()])

# Add totals text in the bottom right
info_text = f"Overall Pals: {totals['Overall Pals']}\n" \
            f"Owned Pals: {totals['Owned Pals']}\n" \
            f"Worker Pals: {totals['Worker Pals']}\n" \
            f"Guilds: {totals['Guilds']}\n" \
            f"Bases: {totals['Bases']}"
ax.text(width - 10, height - 10, info_text, color='red', ha='right', va='bottom', fontsize=96)

# Add top players title
ax.text(width - 10, 10, "Top Players by Pals Caught/Hatched", color='red', ha='right', va='top', fontsize=110)

# Offset for the player's list start below the title
title_offset = 190  # Adjust the offset based on your needs

# Add top 20 players text in the top right below the title
ax.text(width - 10, 10 + title_offset, top_players_text, color='red', ha='right', va='top', fontsize=72)

# Get the current date and format it
current_date = datetime.now().strftime('%Y-%m-%d')

# Add current date in the bottom left
ax.text(10, height - 10, current_date, color='red', ha='left', va='bottom', fontsize=110)

# Remove axis and save the image with high quality
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
plt.savefig('worldbasesmap.png', dpi=100, bbox_inches='tight', pad_inches=0)
plt.close()

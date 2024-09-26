import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np

# Load the main image and icon
main_image_path = 'worldbasesmap.png'
icon_path = 'baseicon.png'
output_image_path = 'worldbasesmap_with_icons.png'
main_image = Image.open(main_image_path)
icon_image = Image.open(icon_path)

# Define the grid boundaries
x_min, x_max = -1000, 1000
y_min, y_max = -1000, 1000

# Calculate the scaling factors to convert world coordinates to image coordinates
height, width = main_image.size
x_scale = width / (x_max - x_min)
y_scale = height / (y_max - y_min)

# Function to convert world coordinates to image coordinates
def to_image_coordinates(x_world, y_world):
    x_img = (x_world - x_min) * x_scale
    y_img = (y_max - y_world) * y_scale  # y-axis is inverted in image coordinates
    return int(x_img), int(y_img)

# Read the CSV file containing base locations
df = pd.read_csv('bases.csv')

# Draw the icon at each base location
draw = ImageDraw.Draw(main_image)
for index, row in df.iterrows():
    for col in ['Base 1', 'Base 2', 'Base 3', 'Base 4']:
        if pd.notna(row[col]):
            x, y = map(int, row[col].split(', '))
            x_img, y_img = to_image_coordinates(x, y)
            # Calculate icon size to fit the location
            icon_size = 90  # Icon size set to fit within the circle radius of 35
            icon_resized = icon_image.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            # Paste the icon onto the main image
            main_image.paste(icon_resized, (x_img - icon_size // 2, y_img - icon_size // 2), icon_resized)

# Save the modified image
main_image.save(output_image_path, 'PNG')

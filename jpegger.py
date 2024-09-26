import os
from PIL import Image

# Configurable variables
target_filesize_mb = 15  # Target file size in megabytes
tolerance = 0.1  # Tolerance for file size (5%)

# Calculate the target file size in bytes
target_filesize = target_filesize_mb * 1024 * 1024

# Load the image
img = Image.open('worldbasesmap_with_icons.png').convert('RGB')  # Convert to RGB for JPEG compatibility

# Function to check if the filesize is within the desired range
def is_within_range(filesize):
    lower_bound = target_filesize * (1 - tolerance)
    upper_bound = target_filesize * (1 + tolerance)
    return lower_bound <= filesize <= upper_bound

# Binary search for the optimal quality
quality = 50
step = 25
min_quality, max_quality = 1, 100  # Valid quality range for JPEG
iteration = 0

while True:
    iteration += 1
    img.save('worldbasesmap_with_icons.jpg', 'JPEG', quality=quality)
    filesize = os.path.getsize('worldbasesmap_with_icons.jpg')
    print(f"Iteration {iteration}: Filesize = {filesize / 1024 / 1024:.2f} MB, Quality = {quality}, Step = {step}")

    if is_within_range(filesize):
        break
    elif filesize > target_filesize:
        max_quality = quality
        quality -= step
    else:
        min_quality = quality
        quality += step

    # Adjust step size
    step = max(1, step // 2)  # Ensure step size does not become zero

print("Final quality setting:", quality)

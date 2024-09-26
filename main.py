import os
import subprocess

# Files to check and delete if exist
files_to_check = ['fix_save.log', 'bases.csv', 'worldbasesmap.png']
for file in files_to_check:
    if os.path.exists(file):
        os.remove(file)

# Define the path to the script and the input file
script_path = "PalworldSaveTools.v0.6.2/fix_save.py"
input_file = "PalworldSaveTools.v0.6.2/level.sav"

# Build the command to run the script with the input file
command = ["python", script_path, input_file]

# Execute the command
result = subprocess.run(command, capture_output=True, text=True)

# Print the output and error (if any)
print("Output:", result.stdout)
if result.stderr:
    print("Error:", result.stderr)

# Run basefinder.py after the first script
basefinder_command = ["python", "basefinder.py"]
result = subprocess.run(basefinder_command, capture_output=True, text=True)

# Print the output and error (if any) from basefinder.py
print("Output from basefinder.py:", result.stdout)
if result.stderr:
    print("Error from basefinder.py:", result.stderr)

# Run mapbases.py after basefinder.py
mapbases_command = ["python", "mapbases.py"]
result = subprocess.run(mapbases_command, capture_output=True, text=True)

# Print the output and error (if any) from mapbases.py
print("Output from mapbases.py:", result.stdout)
if result.stderr:
    print("Error from mapbases.py:", result.stderr)

import os
import subprocess
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Enable message content intent

# Initialize the Discord bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

async def run_scripts():
    # Files to check and delete if exist
    files_to_check = ['players_data.csv', 'bases.csv', 'worldbasesmap.png', 'worldbasesmap.jpg', 'worldbasesmap_with_icons.png', 'worldbasesmap_with_icons.jpg']
    for file in files_to_check:
        if os.path.exists(file):
            os.remove(file)

    # Define the script paths
    script_paths = ['savecopy.py', ('fix_save.py', 'Level.sav'), 'basefinder.py', 'topplayers.py', 'mapbases.py', 'addicons.py', 'jpegger.py']
    for script in script_paths:
        command = ["python", script] if isinstance(script, str) else ["python"] + list(script)
        result = subprocess.run(command, capture_output=False, text=True)
        print(f"Output from {script}:", result.stdout)
        if result.stderr:
            print(f"Error from {script}:", result.stderr)
        await asyncio.sleep(0.5)  # 0.5-second delay between each script execution

async def run_periodic_scripts():
    while True:
        # Define the script paths
        periodic_scripts = ['savecopy.py', ('fix_save.py', 'Level.sav')]
        for script in periodic_scripts:
            command = ["python", script] if isinstance(script, str) else ["python"] + list(script)
            result = subprocess.run(command, capture_output=False, text=True)
            print(f"Output from {script}:", result.stdout)
            if result.stderr:
                print(f"Error from {script}:", result.stderr)
        await asyncio.sleep(600)  # Run every 10 minutes

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check for the specific channel and message content
    if message.channel.id == DISCORD_CHANNEL_ID and message.content.lower() == "showbases":
        await message.channel.send("Generating map...")
        await run_scripts()  # Ensure this is awaited as it is now asynchronous
        await message.channel.send("Map has been generated. Check the results!")

        # Send the image after scripts execution
        if os.path.exists('worldbasesmap_with_icons.jpg'):
            await message.channel.send(file=discord.File('worldbasesmap_with_icons.jpg'))
        else:
            await message.channel.send("Error: Image file not found.")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

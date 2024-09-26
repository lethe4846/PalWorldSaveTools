import discord
import asyncio
import os
from dotenv import load_dotenv
from gamercon_async import GameRCON, GameRCONBase64, ClientError, TimeoutError, InvalidPassword

# Load environment variables
load_dotenv()

# Access environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
LOG_FILES_DIRECTORY = os.getenv('LOG_FILES_DIRECTORY')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

def split_message(content):
    """ Splits the message into parts of up to 43 characters without cutting words. """
    words = content.split()
    current_part = []
    current_length = 0
    for word in words:
        if current_length + len(word) + (1 if current_part else 0) <= 43:
            current_part.append(word)
            current_length += len(word) + (1 if current_part else 0)
        else:
            yield ' '.join(current_part)
            current_part = [word]
            current_length = len(word)
    if current_part:
        yield ' '.join(current_part)

class RconUtility:
    def __init__(self, timeout=30, encoding_info_ttl=50):
        self.timeout = timeout
        self.memory_encoding = {}
        self.encoding_info_ttl = encoding_info_ttl
        self.rcon_host = os.getenv('RCON_HOST', 'default_host')
        self.rcon_port = int(os.getenv('RCON_PORT', 8211))
        self.rcon_pass = os.getenv('RCON_PASS', 'default_password')

    async def rcon_command(self, commands):
        responses = []
        for command in commands:
            print(f"Sending command: {command}")  # Show the command being sent
            try:
                async with GameRCON(self.rcon_host, self.rcon_port, self.rcon_pass, self.timeout) as rcon:
                    response = await rcon.send(command)
                    print(f"RCON Response for '{command}': {response}")  # Detailed response logging
                    responses.append(response)
            except (ClientError, TimeoutError, InvalidPassword) as e:
                print(f"Failed to send RCON command '{command}': {e}")
                responses.append(str(e))
            except Exception as e:
                print(f"An error occurred with command '{command}': {e}")
                responses.append(str(e))
        return responses

class ChatMonitor:
    def __init__(self, client, channel_id, directory):
        self.client = client
        self.channel_id = channel_id
        self.directory = directory
        self.current_file = None
        self.last_pos = 0

    def get_newest_file(self):
        try:
            files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if f.endswith('.txt')]
            if files:
                newest_file = max(files, key=os.path.getmtime)
                return newest_file
            return None
        except Exception as e:
            print(f"Error finding files: {e}")
            return None

    async def check_file(self):
        try:
            newest_file = self.get_newest_file()
            if newest_file:
                if newest_file != self.current_file:
                    self.current_file = newest_file
                    self.last_pos = self.get_initial_position(newest_file)
                    print(f"Switched to new file: {self.current_file}")

                if self.current_file:
                    channel = self.client.get_channel(self.channel_id)
                    with open(self.current_file, 'r', encoding='utf-8') as file:
                        file.seek(self.last_pos)
                        lines = file.readlines()
                        new_position = file.tell()
                        print(f"Read from position {self.last_pos} to {new_position} in file {self.current_file}")
                        self.last_pos = new_position

                        for line in lines:
                            if '(chat)' in line:
                                message = line.split('] ')[2] if '] ' in line else line
                                message = message.replace('(chat)', '').strip()
                                print(f"Sending to Discord: {message}")
                                await channel.send(message)
        except Exception as e:
            print(f"Error reading file: {e}")

    def get_initial_position(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file.seek(0, os.SEEK_END)
                return file.tell()
        except Exception as e:
            print(f"Error accessing file for initial position: {e}")
            return 0

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rcon_utility = RconUtility()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.chat_monitor = ChatMonitor(self, DISCORD_CHANNEL_ID, LOG_FILES_DIRECTORY)
        self.bg_task = self.loop.create_task(self.background_task())

    async def on_message(self, message):
        if message.channel.id == DISCORD_CHANNEL_ID and not message.author.bot:
            sender = message.author.display_name
            if any(ord(c) > 127 for c in sender):
                sender = message.author.name
            content = ''.join(c for c in message.content if ord(c) < 128)
            parts = list(split_message(content))
            commands = [f"broadcast [{sender}]: {parts[0]}"] if parts else []
            commands += [f"broadcast : {part}" for part in parts[1:]]
            responses = await self.rcon_utility.rcon_command(commands)
            for response in responses:
                print(f"RCON Response: {response}")

    async def background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await self.chat_monitor.check_file()
            await asyncio.sleep(2)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = DiscordClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)

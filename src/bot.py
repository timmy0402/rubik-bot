import discord
from discord.ext import commands, tasks
from database.DB_Manager import DatabaseManager
from azure.storage.blob import BlobServiceClient
import os
import requests


class RubiksBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix="/", intents=intents)

        self.db_manager = DatabaseManager()

    async def setup_hook(self):
        # Add the Cog
        from cogs.commands import RubiksCommands

        await self.add_cog(RubiksCommands(self))
        # Sync commands
        await self.tree.sync()

        # Start background tasks
        if not self.keep_database_alive.is_running():
            print("Starting keep-alive task...")
            self.keep_database_alive.start()

        if not self.update_topgg.is_running():
            print("Starting updating topgg...")
            self.update_topgg.start()

        if not self.update_discordbotlist.is_running():
            print("Starting updating discordbotlist...")
            self.update_discordbotlist.start()

    async def on_ready(self):
        print(f"We have logged as an {self.user}")
        # Connect to database
        self.db_manager.connect()

    async def on_disconnect(self):
        self.db_manager.close()

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("!hello"):
            await message.channel.send("Hello!")
        await self.process_commands(message)

    @tasks.loop(minutes=5)
    async def keep_database_alive(self):
        print("Executing keep-alive query...")
        self.db_manager.keep_alive()

    @tasks.loop(minutes=60)
    async def update_topgg(self):
        if os.getenv("ENV", "").upper() != "PROD":
            return
        servers = len(self.guilds)
        id = os.getenv("APPLICATION_ID")
        token = os.getenv("TOPGG_TOKEN")
        url = f"https://top.gg/api/bots/{id}/stats"
        params = {"server_count": servers}
        headers = {"Authorization": token}

        try:
            response = requests.post(url, json=params, headers=headers)
            if response.status_code == 200:
                print(f"Posted server count ({servers}) to Top.gg")
            else:
                print(
                    f"Failed to post to Top.gg: {response.status_code} - {response.text}"
                )
        except Exception as e:
            print(f"Error posting to Top.gg: {e}")

    @tasks.loop(minutes=60)
    async def update_discordbotlist(self):
        if os.getenv("ENV", "").upper() != "PROD":
            return
        servers = len(self.guilds)
        id = os.getenv("APPLICATION_ID")
        token = os.getenv("BOTLIST_TOKEN")
        url = f"https://discordbotlist.com/api/v1/bots/{id}/stats"
        params = {"guilds": servers}
        headers = {"Authorization": token}

        try:
            response = requests.post(url, json=params, headers=headers)
            if response.status_code == 200 or response.status_code == 204:
                print(f"Posted server count ({servers}) to DBL")
            else:
                print(
                    f"Failed to post to DBL: {response.status_code} - {response.text}"
                )
        except Exception as e:
            print(f"Error posting to DBL: {e}")

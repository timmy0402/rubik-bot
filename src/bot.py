import discord
from discord.ext import commands, tasks
from database.DB_Manager import DatabaseManager
from azure.storage.blob import BlobServiceClient
import os
import requests
import logging

logger = logging.getLogger(__name__)


class RubiksBot(commands.Bot):
    """
    Main Bot class for Cube Crafter.
    Handles initialization, database management, and background tasks.
    """

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix="/", intents=intents)

        # Persistent database manager shared across the bot
        self.db_manager = DatabaseManager()

    async def setup_hook(self):
        """
        Setup hook called before the bot starts.
        Registers cogs, syncs commands, and starts background loops.
        """
        # Add the Cog
        from cogs.commands import RubiksCommands

        await self.add_cog(RubiksCommands(self))
        # Sync application commands with Discord
        await self.tree.sync()

        # Start background tasks for database health and stats reporting
        if not self.keep_database_alive.is_running():
            logger.info("Starting keep-alive task...")
            self.keep_database_alive.start()

        if not self.update_topgg.is_running():
            logger.info("Starting updating topgg...")
            self.update_topgg.start()

        if not self.update_discordbotlist.is_running():
            logger.info("Starting updating discordbotlist...")
            self.update_discordbotlist.start()

    async def on_ready(self):
        """
        Triggered when the bot is fully connected and ready.
        """
        logger.info(f"We have logged as an {self.user}")
        # Initialize the shared database connection
        self.db_manager.connect()

    async def on_disconnect(self):
        """
        Cleanup logic when the bot disconnects.
        """
        self.db_manager.close()

    async def on_message(self, message):
        """
        Handle incoming messages.
        """
        if message.author == self.user:
            return
        if message.content.startswith("!hello"):
            await message.channel.send("Hello!")
        await self.process_commands(message)

    @tasks.loop(minutes=5)
    async def keep_database_alive(self):
        """
        Background task to prevent Azure SQL from going idle.
        """
        logger.debug("Executing keep-alive query...")
        self.db_manager.keep_alive()

    @tasks.loop(minutes=60)
    async def update_topgg(self):
        """
        Post bot stats to Top.gg (Production only).
        """
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
                logger.info(f"Posted server count ({servers}) to Top.gg")
            else:
                logger.error(
                    f"Failed to post to Top.gg: {response.status_code} - {response.text}"
                )
        except Exception as e:
            logger.error(f"Error posting to Top.gg: {e}")

    @tasks.loop(minutes=60)
    async def update_discordbotlist(self):
        """
        Post bot stats to DiscordBotList (Production only).
        """
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
                logger.info(f"Posted server count ({servers}) to DBL")
            else:
                logger.error(
                    f"Failed to post to DBL: {response.status_code} - {response.text}"
                )
        except Exception as e:
            logger.error(f"Error posting to DBL: {e}")
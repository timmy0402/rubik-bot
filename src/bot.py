import json
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
        intents.message_content = False
        intents.guilds = True
        self.server_count = 0
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
        if os.getenv("ENV", "").upper() == "PROD":
            await self.tree.sync()
            logger.info("Commands synced globally.")
        else:
            guild_id = os.getenv("GUILD_ID")
            if guild_id:
                dev_guild = discord.Object(id=int(guild_id))
                self.tree.copy_global_to(guild=dev_guild)
                await self.tree.sync(guild=dev_guild)
                logger.info(f"Commands synced with development guild: {guild_id}")
            else:
                logger.warning("GUILD_ID not found in environment. Skipping guild sync.")

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
        try:
            self.db_manager.connect()
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")

    async def on_disconnect(self):
        """
        Cleanup logic when the bot disconnects.
        """
        self.db_manager.close()

    @tasks.loop(minutes=5)
    async def keep_database_alive(self):
        """
        Background task to prevent Azure SQL from going idle.
        """
        logger.debug("Executing keep-alive query...")
        self.db_manager.keep_alive()

    @tasks.loop(minutes=60)
    async def get_servers_count(self):
        """
        Get the current number of servers the bot is in.
        """
        url = "https://discord.com/api/v10/users/@me/guilds?limit=200"

        token = os.getenv("TOKEN")
        payload = {}
        headers = {
        'Authorization': f'Bot {token}',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            guilds = response.json()
            logger.info(f"Retrieved {len(guilds)} guilds from Discord API")
            self.server_count = len(guilds)
        else:
            logger.error(f"Failed to get guilds: {response.status_code} - {response.text}")
        return self.server_count
    
    
    @tasks.loop(minutes=60)
    async def update_topgg(self):
        """
        Post bot stats to Top.gg (Production only).
        """
        if os.getenv("ENV", "").upper() != "PROD":
            return
        servers = self.server_count if self.server_count > 0 else await self.get_servers_count()
        id = os.getenv("APPLICATION_ID")
        token = os.getenv("TOPGG_TOKEN")
        url = f"https://top.gg/api/bots/{id}/stats"
        payload = json.dumps({"server_count": servers})
        headers = {"Authorization": token, "Content-Type": "application/json"}

        try:
            response = requests.request("POST", url, headers=headers, data=payload,)
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
        servers = self.server_count if self.server_count > 0 else await self.get_servers_count()
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
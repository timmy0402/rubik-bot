import discord
from discord.ext import commands
from discord import app_commands
import requests
import base64
from PIL import Image, ImageEnhance
import io
import time
from views.algorithms import AlgorithmsView
from views.timer import TimerView
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class RubiksCommands(commands.Cog):
    """
    Discord Cog containing all Rubik's Cube related commands.
    """

    def __init__(self, bot):
        self.bot = bot
        account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
        access_key = os.getenv("AZURE_STORAGE_ACCESS_KEY")
        self.container = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

        # Initialize Azure Blob service client for algorithm images
        if account_url and access_key:
            self.blob_service_client = BlobServiceClient(
                account_url=account_url, credential=access_key
            )
        else:
            self.blob_service_client = None

    def _log_command_usage(self, command_name):
        """
        Logs the usage of a specific command to the database.
        """
        try:
            self.bot.db_manager.cursor.execute(
                "INSERT INTO CommandLog(CommandName) VALUES(?)", (command_name,)
            )
            self.bot.db_manager.cursor.commit()
        except Exception as e:
            logger.error(f"Log usage failed: {e}")

    @app_commands.command(name="scramble", description="Generate a Rubik's Cube scramble")
    @app_commands.describe(puzzle="Choose the scramble type")
    @app_commands.choices(
        puzzle=[
            app_commands.Choice(name="2x2", value="TWO"),
            app_commands.Choice(name="3x3", value="THREE"),
            app_commands.Choice(name="4x4", value="FOUR"),
            app_commands.Choice(name="5x5", value="FIVE"),
            app_commands.Choice(name="6x6", value="SIX"),
            app_commands.Choice(name="7x7", value="SEVEN"),
            app_commands.Choice(name="pyraminx", value="PYRA"),
            app_commands.Choice(name="square1", value="SQ1"),
            app_commands.Choice(name="megaminx", value="MEGA"),
            app_commands.Choice(name="skewb", value="SKEWB"),
            app_commands.Choice(name="clock", value="CLOCK"),
        ]
    )
    async def scramble(self, interaction: discord.Interaction, puzzle: str):
        """
        Generates a scramble for the selected puzzle type and displays it with an image.
        """
        if interaction.response.is_done():
            logger.warning("Interaction already responded to.")
        else:
            await interaction.response.defer()

            # Log command usage
            self._log_command_usage("scramble")

            # Call external Scrambler API
            url = "https://scrambler-api-apim.azure-api.net/scrambler-api/GetScramble"
            params = {"puzzle": puzzle}

            response = requests.get(url=url, params=params)
            
            if response.status_code != 200:
                await interaction.followup.send("Failed to retrieve scramble. Please try again later.")
                logger.error(f"Scrambler API error: {response.status_code} - {response.text}")
                return
                
            response_json = response.json()
            scramble_string = response_json["scramble"]
            svg_string = response_json["image"]

            # Decode base64 image data
            decode_image = base64.b64decode(svg_string)

            # Load into memory buffer
            png_buffer = io.BytesIO(decode_image)
            png_buffer.seek(0)

            # Process image with Pillow (Resize and enhance contrast)
            with Image.open(png_buffer) as img:
                resized_img = img.resize((500, 300))
                enhancer = ImageEnhance.Contrast(resized_img)
                res = enhancer.enhance(2)

                new_png_buffer = io.BytesIO()
                res.save(new_png_buffer, format="PNG")
                new_png_buffer.seek(0)

            # Create Discord file and embed
            file = discord.File(fp=new_png_buffer, filename="rubiks_cube.png")
            embed = discord.Embed(
                title=f"Your {puzzle} Scramble", description=scramble_string, color=0x0099FF
            )
            embed.set_image(url="attachment://rubiks_cube.png")

            await interaction.followup.send(embed=embed, file=file)

    @app_commands.command(name="oll", description="View all OLL algorithms")
    @app_commands.choices(
        arg=[
            app_commands.Choice(name="Awkward Shape", value="Awkward Shape"),
            app_commands.Choice(name="Big Lightning Bolt", value="Big Lightning Bolt"),
            app_commands.Choice(name="C Shape", value="C Shape"),
            app_commands.Choice(name="Corners Oriented", value="Corners Oriented"),
            app_commands.Choice(name="Cross", value="Cross"),
            app_commands.Choice(name="Dot", value="Dot"),
            app_commands.Choice(name="Fish Shape", value="Fish Shape"),
            app_commands.Choice(name="I Shape", value="I Shape"),
            app_commands.Choice(name="P Shape", value="P Shape"),
            app_commands.Choice(name="Small L Shape", value="Small L Shape"),
            app_commands.Choice(name="Small Lightning Bolt", value="Small Lightning Bolt"),
            app_commands.Choice(name="W Shape", value="W Shape"),
            app_commands.Choice(name="T Shape", value="T Shape"),
        ]
    )
    async def oll(self, interaction: discord.Interaction, arg: str = None):
        """
        Displays OLL algorithms in an interactive paginated view.
        """
        await interaction.response.defer()
        self._log_command_usage("oll")

        algo_view = AlgorithmsView(
            mode="oll",
            user_id=interaction.user.id,
            userName=interaction.user.name,
            initial_group=arg,
            blob_service_client=self.blob_service_client,
            container=self.container,
        )

        if arg and arg not in algo_view.OLL_GROUPS:
            await interaction.followup.send(f"Unknown OLL group: {arg}")
            return

        algo_view.update_buttons()
        embed, file = algo_view.get_embed()

        if file:
            await interaction.followup.send(embed=embed, view=algo_view, file=file)
        else:
            await interaction.followup.send(embed=embed, view=algo_view)

    @app_commands.command(name="pll", description="View all PLL algorithms")
    @app_commands.describe(arg="Optional: Jump to a specific group")
    @app_commands.choices(
        arg=[
            app_commands.Choice(name="Adjacent Corner Swap", value="Adjacent Corner Swap"),
            app_commands.Choice(name="Diagonal Corner Swap", value="Diagonal Corner Swap"),
            app_commands.Choice(name="Edges Only", value="Edges Only"),
        ]
    )
    async def pll(self, interaction: discord.Interaction, arg: str = None):
        """
        Displays PLL algorithms in an interactive paginated view.
        """
        await interaction.response.defer()
        self._log_command_usage("pll")

        algo_view = AlgorithmsView(
            mode="pll",
            user_id=interaction.user.id,
            userName=interaction.user.name,
            initial_group=arg,
            blob_service_client=self.blob_service_client,
            container=self.container,
        )

        if arg and arg not in algo_view.PLL_GROUPS:
            await interaction.followup.send(f"Unknown PLL group: {arg}")
            return

        algo_view.update_buttons()
        embed, file = algo_view.get_embed()

        if file:
            await interaction.followup.send(embed=embed, view=algo_view, file=file)
        else:
            await interaction.followup.send(embed=embed, view=algo_view)

    @app_commands.command(name="stopwatch", description="Time your own solve with an interactive timer")
    @app_commands.describe(arg="Optional: Choose your Puzzle: 3x3, 4x4, etc.")
    @app_commands.choices(
        arg=[
            app_commands.Choice(name="2x2", value="2x2"),
            app_commands.Choice(name="3x3", value="3x3"),
            app_commands.Choice(name="4x4", value="4x4"),
            app_commands.Choice(name="5x5", value="5x5"),
            app_commands.Choice(name="6x6", value="6x6"),
            app_commands.Choice(name="7x7", value="7x7"),
            app_commands.Choice(name="pyraminx", value="PYRA"),
            app_commands.Choice(name="square1", value="SQ1"),
            app_commands.Choice(name="megaminx", value="MEGA"),
            app_commands.Choice(name="skewb", value="SKEWB"),
            app_commands.Choice(name="clock", value="CLOCK"),
        ]
    )
    async def stopwatch(self, interaction: discord.Interaction, arg: str = None):
        """
        Launches an interactive stopwatch for the user to time their solves.
        """
        user_id = interaction.user.id
        user = await self.bot.fetch_user(user_id)
        if arg == None:
            puzzle = "3x3"
        else:
            puzzle = arg

        await interaction.response.defer()
        self._log_command_usage("stopwatch")
        
        try:
            view = TimerView(
                timeout=360,
                user_id=user_id,
                userName=user.name,
                puzzle=puzzle,
                db_manager=self.bot.db_manager,
            )
            await interaction.followup.send(
                "Click **Start** to begin timing. Click **Stop** when finished.", view=view
            )

            message = await interaction.original_response()
            view.message = message

            await view.wait()
            await view.disable_all_items()
        except Exception as e:
            logger.error(f"Stopwatch error: {e}")
            await interaction.followup.send(
                "An error occurred with the timer. Please try again."
            )

    @app_commands.command(name="time", description="Display your recent solve times and averages")
    @app_commands.describe(puzzle="Optional: Filter by puzzle type (3x3, 4x4, etc.)")
    @app_commands.choices(
        puzzle=[
            app_commands.Choice(name="2x2", value="2x2"),
            app_commands.Choice(name="3x3", value="3x3"),
            app_commands.Choice(name="4x4", value="4x4"),
            app_commands.Choice(name="5x5", value="5x5"),
            app_commands.Choice(name="6x6", value="6x6"),
            app_commands.Choice(name="7x7", value="7x7"),
            app_commands.Choice(name="pyraminx", value="PYRA"),
            app_commands.Choice(name="square1", value="SQ1"),
            app_commands.Choice(name="megaminx", value="MEGA"),
            app_commands.Choice(name="skewb", value="SKEWB"),
            app_commands.Choice(name="clock", value="CLOCK"),        
        ]
    )
    async def time(self, interaction: discord.Interaction, puzzle: str = "3x3"):
        """
        Fetches the last 15 solves from the database and calculates Ao5/Ao12.
        """
        await interaction.response.defer(thinking=True)
        self._log_command_usage("time")
        
        try:
            user_id = interaction.user.id
            user = await self.bot.fetch_user(user_id)
            
            # Fetch User Internal ID
            self.bot.db_manager.cursor.execute(
                "SELECT UserID FROM Users WHERE DiscordID = ?", (user_id,)
            )
            db_id = self.bot.db_manager.cursor.fetchval()
            
            if not db_id:
                await interaction.followup.send("You haven't recorded any solves yet!")
                return

            # Fetch last 15 solves for the specific puzzle
            self.bot.db_manager.cursor.execute(
                "SELECT TOP 15 TimeID, SolveTime FROM SolveTimes WHERE UserID=? AND PuzzleType=? ORDER BY TimeID DESC",
                (db_id, puzzle)
            )
            rows = self.bot.db_manager.cursor.fetchall()
            
            if not rows:
                await interaction.followup.send(f"No solve history found for **{puzzle}**.")
                return

            # Helper functions for WCA averages: remove best and worst, then average
            def calculate_wca_avg(times, count):
                if len(times) < count:
                    return None
                subset = sorted(times[:count])
                trimmed = subset[1:-1]
                return sum(trimmed) / len(trimmed)
            
            raw_times = [float(row[1]) for row in rows]
            ao5 = calculate_wca_avg(raw_times, 5)
            ao12 = calculate_wca_avg(raw_times, 12)

            # Build Response Embed
            embed = discord.Embed(
                title=f"{user.name}'s {puzzle} Solve Times",
                description=f"Showing your 15 most recent solves for **{puzzle}**.",
                color=discord.Color.blue(),
            )
            
            ids_str = "\n".join([str(row[0]) for row in rows])
            times_str = "\n".join([f"{row[1]:.02f}s" for row in rows])

            embed.add_field(name="ID", value=ids_str, inline=True)
            embed.add_field(name="Time", value=times_str, inline=True)
            embed.add_field(name="Stats", value=(
                f"**Ao5:** {ao5:.02f}s\n" if ao5 else "**Ao5:** N/A\n"
            ) + (
                f"**Ao12:** {ao12:.02f}s" if ao12 else "**Ao12:** N/A"
            ), inline=True)

            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"Time command error: {e}")
            await interaction.followup.send("Database connection error. Please try again later.")

    @app_commands.command(name="delete_time", description="Delete a specific solve time by ID")
    @app_commands.describe(timeid="The ID of the time to delete (found in /time)")
    async def deleteTime(self, interaction: discord.Interaction, timeid: str):
        """
        Deletes a specific solve time from the user's history.
        """
        await interaction.response.defer(thinking=True)
        self._log_command_usage("delete_time")
        
        try:
            user_id = interaction.user.id
            self.bot.db_manager.cursor.execute(
                "SELECT UserID FROM Users WHERE DiscordID = ?", (user_id,)
            )
            DB_ID = self.bot.db_manager.cursor.fetchval()

            if not DB_ID:
                await interaction.followup.send("History not found.")
                return

            # Security check: Ensure the time belongs to the user
            self.bot.db_manager.cursor.execute(
                "SELECT UserID FROM SolveTimes WHERE TimeID = ?", (timeid,)
            )
            owner_id = self.bot.db_manager.cursor.fetchval()

            if not owner_id:
                await interaction.followup.send("Time ID not found.")
                return

            if owner_id != DB_ID:
                await interaction.followup.send("You cannot delete someone else's time!")
                return

            # Perform deletion
            self.bot.db_manager.cursor.execute(
                "DELETE FROM SolveTimes WHERE TimeID = ?", (timeid,)
            )
            self.bot.db_manager.cursor.commit()

            await interaction.followup.send(f"Successfully deleted record `{timeid}`.")

        except Exception as e:
            logger.error(f"Delete time error: {e}")
            await interaction.followup.send("Error processing deletion.")

    @app_commands.command(name="help", description="View all available commands")
    async def help(self, interaction: discord.Interaction):
        """
        Displays a list of all commands and their descriptions.
        """
        await interaction.response.defer()
        self._log_command_usage("help")

        embed = discord.Embed(
            title="Cube Crafter Help", 
            description="Available commands for tracking and improving your solves:", 
            color=discord.Color.blue()
        )
        embed.add_field(name="/scramble", value="Generate a scramble for various puzzles", inline=False)
        embed.add_field(name="/stopwatch", value="Interactive timer to record your solves", inline=False)
        embed.add_field(name="/time", value="View your recent times and WCA averages", inline=False)
        embed.add_field(name="/delete_time", value="Remove an incorrect time record", inline=False)
        embed.add_field(name="/oll / /pll", value="Reference library for CFOP algorithms", inline=False)

        await interaction.followup.send(embed=embed)
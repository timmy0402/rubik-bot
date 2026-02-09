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
    def __init__(self, bot):
        self.bot = bot
        account_url = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
        access_key = os.getenv("AZURE_STORAGE_ACCESS_KEY")
        self.container = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

        # Initialize blob service client
        if account_url and access_key:
            self.blob_service_client = BlobServiceClient(
                account_url=account_url, credential=access_key
            )
        else:
            self.blob_service_client = None

    def _log_command_usage(self, command_name):
        try:
            self.bot.db_manager.connect()
            self.bot.db_manager.cursor.execute(
                "INSERT INTO CommandLog(CommandName) VALUES(?)", (command_name)
            )
            self.bot.db_manager.cursor.commit()
            self.bot.db_manager.close()
            self.bot.db_manager.close()
        except Exception as e:
            logger.error(f"Log usage failed: {e}")

    @app_commands.command(name="scramble", description="Scramble")
    @app_commands.describe(arg="Choose the scramble type")
    @app_commands.choices(
        arg=[
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
    async def scramble(self, interaction: discord.Interaction, arg: str):
        if interaction.response.is_done():
            logger.warning("Interaction already responded to.")
        else:
            await interaction.response.defer()

            # Insert usage information into database
            self._log_command_usage("scramble")

            url = "https://scrambler-api-apim.azure-api.net/scrambler-api/GetScramble"
            params = {"puzzle": arg}

            logger.info("Getting scramble")
            response = requests.get(url=url, params=params)
            logger.info("Connection code: " + str(response.status_code))
            response = response.json()

            scramble_string = response["scramble"]
            svg_string = response["image"]

            # decode base 64
            decode_image = base64.b64decode(svg_string)

            # save to memory
            png_buffer = io.BytesIO(decode_image)
            png_buffer.seek(0)

            # Open image with Pillow and resize it
            with Image.open(png_buffer) as img:
                resized_img = img.resize((500, 300))

                # Improve contrast
                enhancer = ImageEnhance.Contrast(resized_img)
                res = enhancer.enhance(2)

                new_png_buffer = io.BytesIO()
                res.save(new_png_buffer, format="PNG")
                new_png_buffer.seek(0)

            file = discord.File(fp=new_png_buffer, filename="rubiks_cube.png")
            embed = discord.Embed(
                title="Your scramble", description=scramble_string, color=0x0099FF
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
            app_commands.Choice(
                name="Small Lightning Bolt", value="Small Lightning Bolt"
            ),
            app_commands.Choice(name="W Shape", value="W Shape"),
            app_commands.Choice(name="T Shape", value="T Shape"),
        ]
    )
    async def oll(self, interaction: discord.Interaction, arg: str = None):
        """
        Shows a list of OLL algorithms in an interactive view.
        """
        await interaction.response.defer()

        self._log_command_usage("oll")

        # Instantiate AlgorithmsView with initial group if arg provided
        algo_view = AlgorithmsView(
            mode="oll",
            user_id=interaction.user.id,
            userName=interaction.user.name,
            initial_group=arg,
            blob_service_client=self.blob_service_client,
            container=self.container,
        )

        if arg and arg not in algo_view.OLL_GROUPS:
            await interaction.followup.send(f"Unknown group: {arg}")
            return

        # Update buttons state initially
        algo_view.update_buttons()
        # get_embed now returns a tuple
        embed, file = algo_view.get_embed()

        if file:
            await interaction.followup.send(embed=embed, view=algo_view, file=file)
        else:
            await interaction.followup.send(embed=embed, view=algo_view)

    @app_commands.command(name="pll", description="View all PLL algorithms")
    @app_commands.describe(arg="Optional: Jump to a specific group")
    @app_commands.choices(
        arg=[
            app_commands.Choice(
                name="Adjacent Corner Swap", value="Adjacent Corner Swap"
            ),
            app_commands.Choice(
                name="Diagonal Corner Swap", value="Diagonal Corner Swap"
            ),
            app_commands.Choice(name="Edges Only", value="Edges Only"),
        ]
    )
    async def pll(self, interaction: discord.Interaction, arg: str = None):
        """
        Shows a list of PLL algorithms in an interactive view.
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
            await interaction.followup.send(f"Unknown group: {arg}")
            return

        # Update buttons state initially
        algo_view.update_buttons()
        # get_embed now returns a tuple
        embed, file = algo_view.get_embed()

        if file:
            await interaction.followup.send(embed=embed, view=algo_view, file=file)
        else:
            await interaction.followup.send(embed=embed, view=algo_view)

    @app_commands.command(
        name="stopwatch", description="Time your own solve with timer"
    )
    async def stopwatch(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user = await self.bot.fetch_user(user_id)

        await interaction.response.defer()

        # Insert usage information into database
        self._log_command_usage("stopwatch")
        try:
            view = TimerView(timeout=90, user_id=user_id, userName=user.name)
            await interaction.followup.send(
                "Click a button to start or stop the timer.", view=view
            )

            message = await interaction.original_response()
            view.message = message

            await view.wait()
            await view.disable_all_items()
        except Exception as e:
            await interaction.followup.send(
                "Database Inactive. Try again in 5-20 seconds"
            )

    @app_commands.command(
        name="time", description="Display time of your last 10 solves"
    )
    async def time(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        # Insert usage information into database
        self._log_command_usage("time")
        try:
            self.bot.db_manager.connect()
            user_id = interaction.user.id
            user = await self.bot.fetch_user(user_id)
            self.bot.db_manager.cursor.execute(
                "SELECT UserID FROM Users WHERE DiscordID = ?", (user_id,)
            )
            DB_ID = self.bot.db_manager.cursor.fetchval()
            self.bot.db_manager.cursor.execute(
                "SELECT TimeID, SolveTime FROM SolveTimes WHERE UserID=? ORDER BY TimeID DESC",
                (DB_ID),
            )
            rows = self.bot.db_manager.cursor.fetchall()
            # will return [(timeid, Decimal('solveTime')), (timeid1, Decimal('solveTime1'))]
            def calulate_ao5(times):
                if len(times) < 5:
                    return None
                sorted_times = sorted(times)
                return sum(sorted_times[1:4]) / 3
            def calculate_ao12(times):
                if len(times) < 12:
                    return None
                sorted_times = sorted(times)
                return sum(sorted_times[1:11]) / 10
            
            if len(rows) >= 12:
                solve_times = [float(row[1]) for row in rows[:12]]
                ao5 = calulate_ao5(solve_times)
                ao12 = calculate_ao12(solve_times)
            elif len(rows) >= 5:
                solve_times = [float(row[1]) for row in rows[:5]]
                ao5 = calulate_ao5(solve_times)
                ao12 = None
            else:
                ao5 = None
                ao12 = None
            self.bot.db_manager.close()

            # Create embed respond
            embed = discord.Embed(
                title=str(user.name) + "'s solve times: ",
                description="Your last 15 solve times",
                color=discord.Color.blue(),
            )
            # Prepare fields for embed
            time_ids = "\n".join([str(row[0]) for row in rows])
            solve_times = "\n".join([f"{row[1]:.02f}" for row in rows])

            # Added fields
            embed.add_field(name="TimeID", value=time_ids, inline=True)
            embed.add_field(name="SolveTimes", value=solve_times, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)  # Empty field for spacing
            embed.add_field(name="Ao5", value=f"{ao5:.02f}" if ao5 else "N/A", inline=True)
            embed.add_field(name="Ao12", value=f"{ao12:.02f}" if ao12 else "N/A", inline=True)

            await interaction.followup.send(embed=embed)
        except discord.errors.NotFound:
            # Handle expired interaction
            if interaction.channel:
                await interaction.channel.send(
                    "The interaction has expired. Please try the command again."
                )
        except Exception as e:
            await interaction.followup.send(
                "Database Inactive. Try again in 5-20 seconds"
            )

    @app_commands.command(
        name="delete_time", description="Delete a time from your solve times"
    )
    @app_commands.describe(timeid="The ID of the time to delete")
    async def deleteTime(self, interaction: discord.Interaction, timeid: str):
        # Defer immediately to prevent interaction timeout
        await interaction.response.defer(thinking=True)

        # Insert usage information into database
        self._log_command_usage("delete_time")
        try:
            # Connect to the database
            self.bot.db_manager.connect()

            # Get the user ID from Discord interaction
            user_id = interaction.user.id
            self.bot.db_manager.cursor.execute(
                "SELECT UserID FROM Users WHERE DiscordID = ?", (user_id,)
            )
            DB_ID = self.bot.db_manager.cursor.fetchval()

            # If no user ID is found, respond and stop
            if not DB_ID:
                await interaction.followup.send(
                    "You don't have any recorded times yet. Use the stopwatch to add some."
                )
                self.bot.db_manager.close()
                return

            # Check if the provided TimeID exists in the SolveTimes table
            self.bot.db_manager.cursor.execute(
                "SELECT UserID FROM SolveTimes WHERE TimeID = ?", (timeid,)
            )
            temp_id = self.bot.db_manager.cursor.fetchval()

            if not temp_id:
                await interaction.followup.send(
                    "This TimeID doesn't exist. Please check the ID and try again."
                )
                self.bot.db_manager.close()
                return

            # If the time does not belong to the user, respond with an error
            if temp_id != DB_ID:
                await interaction.followup.send(
                    "This is not your time. Please try a different one."
                )
                self.bot.db_manager.close()
                return

            # Delete the time entry from the database
            self.bot.db_manager.cursor.execute(
                "DELETE FROM SolveTimes WHERE TimeID = ?", (timeid,)
            )
            self.bot.db_manager.cursor.commit()
            self.bot.db_manager.close()

            # Send confirmation message
            await interaction.followup.send(
                f"Time with ID `{timeid}` has been successfully deleted."
            )

        except discord.errors.NotFound:
            # Handle expired interaction if the user takes too long
            if interaction.channel:
                await interaction.channel.send(
                    "The interaction has expired. Please try again."
                )
        except Exception as e:
            # Catch any other errors
            await interaction.followup.send(
                "An error occurred while processing your request. Please try again later."
            )
            logger.error(f"Error in delete_time: {e}")

    @app_commands.command(name="help", description="view all command")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Insert usage information into database
        self._log_command_usage("help")

        embed = discord.Embed(
            title="Help", description="Command list", color=discord.Color.blue()
        )
        embed.add_field(
            name="scramble", value="Create a scramble with any WCA cube", inline=False
        )
        embed.add_field(
            name="stopwatch", value="Create a stopwatch for your solve", inline=False
        )
        embed.add_field(
            name="time", value="Show the time for your last 10 solves", inline=False
        )
        embed.add_field(
            name="delete_time", value="Delete a time by TimeID", inline=False
        )

        await interaction.followup.send(embed=embed)

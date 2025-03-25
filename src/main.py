import discord
from discord.ext import commands, tasks
from discord import app_commands

import topgg

import os
from dotenv import load_dotenv

import requests

import base64
from PIL import Image, ImageEnhance
import io

import timer

from DB_Manager import DatabaseManager


def insertUsageToDB(commandName):
    try:
        db_manager.connect()
        db_manager.cursor.execute(
            "INSERT INTO CommandLog(CommandName) VALUES(?)", (commandName)
        )
        db_manager.cursor.commit()
        db_manager.close()
    except Exception as e:
        print("Log failed")


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="/", intents=intents)

cursor = None

db_manager = DatabaseManager()


@bot.event
async def on_ready():
    print(f"We have logged as an {bot.user}")
    client = topgg.DBLClient(token=os.getenv("topgg"), bot=bot)
    print("TOPGG number updated")
    await client.post_guild_count(len(bot.guilds))
    await client.close()
    # Uncommented to make database run 24/7
    db_manager.connect()
    if not keep_database_alive.is_running():
        print("Starting keep-alive task...")
        keep_database_alive.start()
    await bot.tree.sync()


@bot.event
async def on_guild_join(guild):
    client = topgg.DBLClient(token=os.getenv("topgg"), bot=bot)
    await client.post_guild_count(len(bot.guilds))
    await client.close()
    print("Guild joined")


@bot.event
async def on_disconnect():
    db_manager.close()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")
    await bot.process_commands(message)


@bot.tree.command(name="scramble", description="Scramble")
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
async def scramble(interaction: discord.Interaction, arg: str):
    if interaction.response.is_done():
        print("Interaction already responded to.")
    else:
        await interaction.response.defer()

        # Insert usage information into database
        insertUsageToDB("scramble")

        url = "https://scrambler-api-apim.azure-api.net/scrambler-api/GetScramble"
        params = {"puzzle": arg}

        print("Getting scramble")
        response = requests.get(url=url, params=params)
        print("Connection code: " + str(response.status_code))
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


@bot.tree.command(name="stopwatch", description="Time your own solve with timer")
async def stopwatch(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = await bot.fetch_user(user_id)

    await interaction.response.defer()

    # Insert usage information into database
    insertUsageToDB("stopwatch")
    try:
        view = timer.TimerView(timeout=90, user_id=user_id, userName=user.name)
        await interaction.followup.send(
            "Click a button to start or stop the timer.", view=view
        )

        message = await interaction.original_response()
        view.message = message

        await view.wait()
        await view.disable_all_items()
    except Exception as e:
        await interaction.followup.send("Database Inactive. Try again in 5-20 seconds")


@bot.tree.command(name="time", description="Display time of your last 10 solves")
async def time(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    # Insert usage information into database
    insertUsageToDB("time")
    try:
        db_manager.connect()
        user_id = interaction.user.id
        user = await bot.fetch_user(user_id)
        db_manager.cursor.execute(
            "SELECT UserID FROM Users WHERE DiscordID = ?", (user_id,)
        )
        DB_ID = db_manager.cursor.fetchval()
        db_manager.cursor.execute(
            "SELECT TimeID, SolveTime FROM SolveTimes WHERE UserID=? ORDER BY TimeID DESC",
            (DB_ID),
        )
        rows = db_manager.cursor.fetchall()
        # will return [(timeid, Decimal('solveTime')), (timeid1, Decimal('solveTime1'))]
        db_manager.close()

        # Create embed respond
        embed = discord.Embed(
            title=str(user.name) + "'s solve times: ",
            description="Your last 10 solve times",
            color=discord.Color.blue(),
        )
        # Prepare fields for embed
        time_ids = "\n".join([str(row[0]) for row in rows])
        solve_times = "\n".join([f"{row[1]:.02f}" for row in rows])

        # Added fields
        embed.add_field(name="TimeID", value=time_ids, inline=True)
        embed.add_field(name="SolveTimes", value=solve_times, inline=True)

        await interaction.followup.send(embed=embed)
    except discord.errors.NotFound:
        # Handle expired interaction
        if interaction.channel:
            await interaction.channel.send(
                "The interaction has expired. Please try the command again."
            )
    except Exception as e:
        await interaction.followup.send("Database Inactive. Try again in 5-20 seconds")


@bot.tree.command(name="delete_time", description="Delete a time from your solve times")
@app_commands.describe(timeid="The ID of the time to delete")
async def deleteTime(interaction: discord.Interaction, timeid: str):
    # Defer immediately to prevent interaction timeout
    await interaction.response.defer(thinking=True)

    # Insert usage information into database
    insertUsageToDB("delete_time")
    try:
        # Connect to the database
        db_manager.connect()

        # Get the user ID from Discord interaction
        user_id = interaction.user.id
        db_manager.cursor.execute(
            "SELECT UserID FROM Users WHERE DiscordID = ?", (user_id,)
        )
        DB_ID = db_manager.cursor.fetchval()

        # If no user ID is found, respond and stop
        if not DB_ID:
            await interaction.followup.send(
                "You don't have any recorded times yet. Use the stopwatch to add some."
            )
            db_manager.close()
            return

        # Check if the provided TimeID exists in the SolveTimes table
        db_manager.cursor.execute(
            "SELECT UserID FROM SolveTimes WHERE TimeID = ?", (timeid,)
        )
        temp_id = db_manager.cursor.fetchval()

        if not temp_id:
            await interaction.followup.send(
                "This TimeID doesn't exist. Please check the ID and try again."
            )
            db_manager.close()
            return

        # If the time does not belong to the user, respond with an error
        if temp_id != DB_ID:
            await interaction.followup.send(
                "This is not your time. Please try a different one."
            )
            db_manager.close()
            return

        # Delete the time entry from the database
        db_manager.cursor.execute("DELETE FROM SolveTimes WHERE TimeID = ?", (timeid,))
        db_manager.cursor.commit()
        db_manager.close()

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
        print(f"Error in delete_time: {e}")


@bot.tree.command(name="help", description="view all command")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()

    # Insert usage information into database
    insertUsageToDB("help")

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
    embed.add_field(name="delete_time", value="Delete a time by TimeID", inline=False)

    await interaction.followup.send(embed=embed)


# Uncommented to make DB run 24/7
@tasks.loop(minutes=5)
async def keep_database_alive():
    print("Executing keep-alive query...")
    db_manager.keep_alive()


bot.run(os.getenv("TOKEN"))

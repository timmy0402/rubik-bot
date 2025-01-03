import discord
from discord.ext import commands, tasks
from discord import app_commands

import topgg

import os
from dotenv import load_dotenv

from pyTwistyScrambler import scrambler222,scrambler333,scrambler444,scrambler555,scrambler666, scrambler777, megaminxScrambler, squareOneScrambler, skewbScrambler,clockScrambler,pyraminxScrambler

import pyodbc

import timer
from cube import Cube
from draw import draw_rubiks_cube

from DB_Manager import DatabaseManager

def insertUsageToDB(commandName):
    try:
        db_manager.connect()
        db_manager.cursor.execute("INSERT INTO CommandLog(CommandName) VALUES(?)",(commandName))
        db_manager.cursor.commit()
        db_manager.close()
    except Exception as e:
        print("Log failed")

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='/', intents=intents)

cursor = None

db_manager = DatabaseManager()

@bot.event
async def on_ready():
    print(f'We have logged as an {bot.user}')
    client = topgg.DBLClient(token=os.getenv("TOPGG"),bot=bot)
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
    client = topgg.DBLClient(token=os.getenv("TOPGG"),bot=bot)
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
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)

@bot.tree.command(name="scramble", description="Scramble")
@app_commands.describe(arg="Choose the scramble type")
@app_commands.choices(arg=[
    app_commands.Choice(name="2x2", value="2x2"),
    app_commands.Choice(name="3x3", value="3x3"),
    app_commands.Choice(name="4x4", value="4x4"),
    app_commands.Choice(name="5x5", value="5x5"),
    app_commands.Choice(name="6x6", value="6x6"),
    app_commands.Choice(name="7x7", value="7x7"),
    app_commands.Choice(name="pyraminx", value="pyraminx"),
    app_commands.Choice(name="square1", value="square1"),
    app_commands.Choice(name="megaminx", value="megaminx"),
    app_commands.Choice(name="skewb", value="skewb"),
    app_commands.Choice(name="clock", value="clock")
])
async def scramble(interaction : discord.Interaction, arg: str):
    await interaction.response.defer()
    
    # Insert usage information into database
    insertUsageToDB('scramble')

    if(arg == '2x2'):
        # Scramble Cube & draw image
        scramble_string = scrambler222.get_WCA_scramble()
        rubik_cube = Cube(size=2)
        rubik_cube.scrambleCube(scramble_string)
        img_bytes = draw_rubiks_cube(rubik_cube)

        image_filename = "rubiks_cube.png"

        # Upload Image
        file = discord.File(fp=img_bytes,filename=image_filename)
        embed = discord.Embed(title="Your scramble", description=scramble_string,color=0x0099FF)
        embed.set_image(url="attachment://rubiks_cube.png")

        await interaction.followup.send(embed=embed, file=file)
    elif(arg == '3x3'):
        # Scramble Cube & draw image
        scramble_string = scrambler333.get_WCA_scramble()
        rubik_cube = Cube(size=3)
        rubik_cube.scrambleCube(scramble_string)
        img_bytes = draw_rubiks_cube(rubik_cube)

        image_filename = "rubiks_cube.png"

        # Upload Image
        file = discord.File(fp=img_bytes,filename=image_filename)
        embed = discord.Embed(title="Your scramble", description=scramble_string,color=0x0099FF)
        embed.set_image(url="attachment://rubiks_cube.png")

        await interaction.followup.send(embed=embed, file=file)

    elif(arg == '4x4'):
        # Scramble Cube & draw image
        scramble_string = scrambler444.get_WCA_scramble()
        rubik_cube = Cube(size=4)
        rubik_cube.scrambleCube(scramble_string)
        img_bytes = draw_rubiks_cube(rubik_cube)

        image_filename = "rubiks_cube.png"

        # Upload Image
        file = discord.File(fp=img_bytes,filename=image_filename)
        embed = discord.Embed(title="Your scramble", description=scramble_string,color=0x0099FF)
        embed.set_image(url="attachment://rubiks_cube.png")

        await interaction.followup.send(embed=embed, file=file)
    elif(arg == '5x5'):
        # Scramble Cube & draw image
        scramble_string = scrambler555.get_WCA_scramble()
        rubik_cube = Cube(size=5)
        rubik_cube.scrambleCube(scramble_string)
        img_bytes = draw_rubiks_cube(rubik_cube)

        image_filename = "rubiks_cube.png"

        # Upload Image
        file = discord.File(fp=img_bytes,filename=image_filename)
        embed = discord.Embed(title="Your scramble", description=scramble_string,color=0x0099FF)
        embed.set_image(url="attachment://rubiks_cube.png")

        await interaction.followup.send(embed=embed, file=file)
    elif(arg == '6x6'):
        # Scramble Cube & draw image
        scramble_string = scrambler666.get_WCA_scramble()
        rubik_cube = Cube(size=6)
        rubik_cube.scrambleCube(scramble_string)
        img_bytes = draw_rubiks_cube(rubik_cube)

        image_filename = "rubiks_cube.png"

        # Upload Image
        file = discord.File(fp=img_bytes,filename=image_filename)
        embed = discord.Embed(title="Your scramble", description=scramble_string,color=0x0099FF)
        embed.set_image(url="attachment://rubiks_cube.png")

        await interaction.followup.send(embed=embed, file=file)
    elif(arg == '7x7'):
        # Scramble Cube & draw image
        scramble_string = scrambler777.get_WCA_scramble()
        rubik_cube = Cube(size=7)
        rubik_cube.scrambleCube(scramble_string)
        img_bytes = draw_rubiks_cube(rubik_cube)

        image_filename = "rubiks_cube.png"

        # Upload Image
        file = discord.File(fp=img_bytes,filename=image_filename)
        embed = discord.Embed(title="Your scramble", description=scramble_string,color=0x0099FF)
        embed.set_image(url="attachment://rubiks_cube.png")

        await interaction.followup.send(embed=embed, file=file)
        await interaction.followup.send(scramble_text)
    elif(arg == 'pyraminx'):
        scramble_text = pyraminxScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'megaminx'):
        scramble_text = megaminxScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'clock'):
        scramble_text = clockScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'square1'):
        scramble_text = squareOneScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'skewb'):
        scramble_text = skewbScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    
@bot.tree.command(name="stopwatch",description="Time your own solve with timer")
async def stopwatch(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = await bot.fetch_user(user_id)

    await interaction.response.defer()

    # Insert usage information into database
    insertUsageToDB('stopwatch')
    try:
        view = timer.TimerView(timeout=90,user_id=user_id,userName=user.name)        
        await interaction.followup.send("Click a button to start or stop the timer.", view=view)

        message = await interaction.original_response()
        view.message = message
        
        await view.wait()
        await view.disable_all_items()
    except Exception as e:
        await interaction.followup.send("Database Inactive. Try again in 5-20 seconds")


@bot.tree.command(name="time",description="Display time of your last 10 solves")
async def time(interaction : discord.Interaction):
    await interaction.response.defer(thinking=True)

    # Insert usage information into database
    insertUsageToDB('time')
    try:
        db_manager.connect()
        user_id = interaction.user.id
        user = await bot.fetch_user(user_id)
        db_manager.cursor.execute('SELECT UserID FROM Users WHERE DiscordID = ?', (user_id,))
        DB_ID = db_manager.cursor.fetchval()
        db_manager.cursor.execute('SELECT TimeID, SolveTime FROM SolveTimes WHERE UserID=? ORDER BY TimeID DESC',(DB_ID))
        rows = db_manager.cursor.fetchall()
        # will return [(timeid, Decimal('solveTime')), (timeid1, Decimal('solveTime1'))]
        db_manager.close()

        # Create embed respond
        embed = discord.Embed(
            title= str(user.name) + "'s solve times: ",
            description="Your last 10 solve times",
            color=discord.Color.blue()
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
            await interaction.channel.send("The interaction has expired. Please try the command again.")
    except Exception as e:
        await interaction.followup.send("Database Inactive. Try again in 5-20 seconds")
        

@bot.tree.command(name="delete_time",description="Delete a time from your solve times")
@app_commands.describe(timeid="The ID of the time to delete")
async def deleteTime(interaction: discord.Interaction, timeid: str):
    # Defer immediately to prevent interaction timeout
    await interaction.response.defer(thinking=True)

    # Insert usage information into database
    insertUsageToDB('delete_time')
    try:
        # Connect to the database
        db_manager.connect()

        # Get the user ID from Discord interaction
        user_id = interaction.user.id
        db_manager.cursor.execute('SELECT UserID FROM Users WHERE DiscordID = ?', (user_id,))
        DB_ID = db_manager.cursor.fetchval()

        # If no user ID is found, respond and stop
        if not DB_ID:
            await interaction.followup.send("You don't have any recorded times yet. Use the stopwatch to add some.")
            db_manager.close()
            return

        # Check if the provided TimeID exists in the SolveTimes table
        db_manager.cursor.execute('SELECT UserID FROM SolveTimes WHERE TimeID = ?', (timeid,))
        temp_id = db_manager.cursor.fetchval()

        if not temp_id:
            await interaction.followup.send("This TimeID doesn't exist. Please check the ID and try again.")
            db_manager.close()
            return

        # If the time does not belong to the user, respond with an error
        if temp_id != DB_ID:
            await interaction.followup.send("This is not your time. Please try a different one.")
            db_manager.close()
            return

        # Delete the time entry from the database
        db_manager.cursor.execute('DELETE FROM SolveTimes WHERE TimeID = ?', (timeid,))
        db_manager.cursor.commit()
        db_manager.close()

        # Send confirmation message
        await interaction.followup.send(f"Time with ID `{timeid}` has been successfully deleted.")

    except discord.errors.NotFound:
        # Handle expired interaction if the user takes too long
        if interaction.channel:
            await interaction.channel.send("The interaction has expired. Please try again.")
    except Exception as e:
        # Catch any other errors
        await interaction.followup.send("An error occurred while processing your request. Please try again later.")
        print(f"Error in delete_time: {e}")



@bot.tree.command(name="help",description="view all command")
async def help(interaction : discord.Interaction):
    await interaction.response.defer()

    # Insert usage information into database
    insertUsageToDB('help')

    embed = discord.Embed(
        title="Help",
        description="Command list",
        color=discord.Color.blue()
    )
    embed.add_field(name="scramble",value="Create a scramble with any WCA cube",inline=False)
    embed.add_field(name="stopwatch",value="Create a stopwatch for your solve",inline=False)
    embed.add_field(name="time",value="Show the time for your last 10 solves",inline=False)
    embed.add_field(name="delete_time",value="Delete a time by TimeID",inline=False)

    await interaction.followup.send(embed=embed)

# Uncommented to make DB run 24/7
@tasks.loop(minutes=5)
async def keep_database_alive():
    print("Executing keep-alive query...")
    db_manager.keep_alive()



bot.run(os.getenv('TOKEN'))

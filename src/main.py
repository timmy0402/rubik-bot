import discord
from discord.ext import commands, tasks
from discord import app_commands

import os
from dotenv import load_dotenv

from pyTwistyScrambler import scrambler222,scrambler333,scrambler444,scrambler555,scrambler666, scrambler777, megaminxScrambler, squareOneScrambler, skewbScrambler,clockScrambler,pyraminxScrambler

import pyodbc

import timer
from cube import Cube
from draw import draw_rubiks_cube

from DB_Manager import DatabaseManager

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

cursor = None

db_manager = DatabaseManager()

@bot.event
async def on_ready():
    print(f'We have logged as an {bot.user}')
    # Uncommented to make database run 24/7
    #    db_manager.connect()
    #if not keep_database_alive.is_running():
    #    print("Starting keep-alive task...")
    #    keep_database_alive.start()
    await bot.tree.sync()

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
    app_commands.Choice(name="4x4", value="5x5"),
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
    if(arg == '2x2'):
        scramble_string = scrambler222.get_WCA_scramble()
        rubik_cube = Cube(size=2)
        await interaction.response.send_message(scrambler222.get_WCA_scramble())
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

        await interaction.response.send_message(embed=embed, file=file)

    elif(arg == '4x4'):
        await interaction.response.defer()
        scramble_text = scrambler444.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == '5x5'):
        await interaction.response.defer()
        scramble_text = scrambler555.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == '6x6'):
        await interaction.response.defer()
        scramble_text = scrambler666.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == '7x7'):
        await interaction.response.defer()
        scramble_text = scrambler777.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'pyraminx'):
        await interaction.response.defer()
        scramble_text = pyraminxScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'megaminx'):
        await interaction.response.defer()
        scramble_text = megaminxScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'clock'):
        await interaction.response.defer()
        scramble_text = clockScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'square1'):
        await interaction.response.defer()
        scramble_text = squareOneScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    elif(arg == 'skewb'):
        await interaction.response.defer()
        scramble_text = skewbScrambler.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    
@bot.tree.command(name="stopwatch",description="Time your own solve with timer")
async def stopwatch(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = await bot.fetch_user(user_id)
    view = timer.TimerView(timeout=90,user_id=user_id,userName=user.name)
    await interaction.response.defer()
    
    await interaction.followup.send("Click a button to start or stop the timer.", view=view)

    message = await interaction.original_response()
    view.message = message
    
    await view.wait()
    await view.disable_all_items()

@bot.tree.command(name="time",description="Display time of your last 10 solves")
async def time(interaction : discord.Interaction):
    try:
        await interaction.response.defer()
        db_manager.connect()
        user_id = interaction.user.id
        user = await bot.fetch_user(user_id)
        db_manager.cursor.execute('SELECT UserID FROM Users WHERE DiscordID = ?', (user_id,))
        DB_ID = db_manager.cursor.fetchval()
        db_manager.cursor.execute('SELECT TimeID, SolveTime FROM SolveTimes WHERE UserID=? ORDER BY TimeID DESC',(DB_ID))
        rows = db_manager.cursor.fetchall()
        embed = discord.Embed(
            title= str(user.name) + "'s solve times: ",
            description="Your last 10 solve times",
            color=discord.Color.blue()
        )
        embed.add_field(name="TimeID", value="", inline=True)
        embed.add_field(name="SolveTimes", value="", inline=True)

        for row in rows:
            embed.add_field(name="", value=f"`{str(row[0]):<10} {str(row[1]):<10}`", inline=False)

        db_manager.close()
        await interaction.followup.send(embed=embed)
    except pyodbc.Error as e:
        await interaction.followup.send("Database Inactive. Try again in 5-20 seconds")
        

@bot.tree.command(name="delete_time",description="Delete a time from your solve times")
@app_commands.describe(timeid="The ID of the time to delete")
async def deleteTime(interaction : discord.Interaction,timeid : str):
    db_manager.connect()
    user_id = interaction.user.id
    db_manager.cursor.execute('SELECT UserID FROM Users WHERE DiscordID = ?', (user_id,))
    DB_ID = db_manager.cursor.fetchval()
    if not DB_ID:
        await interaction.response.send_message("You don't have a time yet, use stopwatch to add some")
        return
    db_manager.cursor.execute('SELECT UserID FROM SolveTimes WHERE TimeID = ?',(timeid))
    temp_id = db_manager.cursor.fetchval()
    if not temp_id:
        await interaction.response.send_message("You don't have a time yet, use stopwatch to add some")
        return
    if temp_id != DB_ID:
        await interaction.response.send_message("This is not your time, try a different one")
        return
    db_manager.cursor.execute('DELETE FROM SolveTimes WHERE TimeID = ?',(timeid))
    db_manager.cursor.commit()
    db_manager.close()
    await interaction.response.send_message(f"`{str(timeid)}`" + " is deleted")



@bot.tree.command(name="help",description="view all command")
async def help(interaction : discord.Interaction):
    embed = discord.Embed(
        title="Help",
        description="Command list",
        color=discord.Color.blue()
    )
    embed.add_field(name="scramble",value="Create a scramble with any WCA cube",inline=False)
    embed.add_field(name="stopwatch",value="Create a stopwatch for your solve",inline=False)
    embed.add_field(name="time",value="Show the time for your last 10 solves",inline=False)
    embed.add_field(name="delete_time",value="Delete a time by TimeID",inline=False)

    await interaction.response.send_message(embed=embed)

# Uncommented to make DB run 24/7
#@tasks.loop(minutes=5)
#async def keep_database_alive():
#    print("Executing keep-alive query...")
#    db_manager.keep_alive()



bot.run(os.getenv('TEST_TOKEN'))
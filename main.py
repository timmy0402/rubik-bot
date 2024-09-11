import discord
from discord.ext import commands
from discord import app_commands

import os
from dotenv import load_dotenv

from pyTwistyScrambler import scrambler222, scrambler333, scrambler444, scrambler555, scrambler666, scrambler777

import timer
from cube import Cube
from draw import draw_rubiks_cube

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged as an {bot.user}')
    await bot.tree.sync()


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
    app_commands.Choice(name="7x7", value="7x7")
])
async def scramble(interaction : discord.Interaction, arg: str):
    if(arg == '2x2'):
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
    
@bot.tree.command(name="stopwatch",description="Time your own solve with timer")
async def stopwatch(interaction: discord.Interaction):
    view = timer.TimerView(timeout=90)
    message = await interaction.response.send_message(view=view)
    view.message = message
    
    await view.wait()
    await view.disable_all_items()


bot.run(os.getenv('TOKEN'))
import discord
from discord.ext import commands
from discord import app_commands

import os
from dotenv import load_dotenv

from pyTwistyScrambler import scrambler333, scrambler444

import timer
import cube

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
    app_commands.Choice(name="3x3", value="3x3"),
    app_commands.Choice(name="4x4", value="4x4")
])
async def scramble(interaction : discord.Interaction, arg: str):
    if(arg == '3x3'):
        scramble_string = scrambler333.get_WCA_scramble()
        visual = cube.Cube()
        visual.scrambleCube(scramble_string)

        embed = discord.Embed(title="Your scramble", description=scramble_string,color=0x0099FF)
        embed.set_image(url="attachment://rubiks_cube.png")

        await interaction.response.send_message(embed=embed)

        # Delete the image file after use
        try:
            os.remove("rubiks_cube.png")
        except Exception as e:
            await interaction.followup.send(f"Failed to delete image file: {e}")

    elif(arg == '4x4'):
        await interaction.response.defer()
        scramble_text = scrambler444.get_WCA_scramble()
        await interaction.followup.send(scramble_text)
    

@bot.command()
async def button(ctx):
    view = discord.ui.View()
    button = discord.ui.Button(label="click me")
    view.add_item(button)
    await ctx.send(view=view)

@bot.command()
async def stopwatch(ctx):
    view = timer.TimerView(timeout=90)
    message = await ctx.send(view=view)
    view.message = message
    
    await view.wait()
    await view.disable_all_items()


bot.run(os.getenv('TOKEN'))
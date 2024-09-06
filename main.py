import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from pyTwistyScrambler import scrambler333, scrambler444
import timer

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
async def scramble(ctx, arg: str):
    if(arg == '3x3'):
        await ctx.response.send_message(scrambler333.get_WCA_scramble())
    elif(arg == '4x4'):
        await ctx.response.defer()
        scramble_text = scrambler444.get_WCA_scramble()
        await ctx.followup.send(scramble_text)
    

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
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pyTwistyScrambler import scrambler333, scrambler444

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged as an {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)

@bot.command()
async def scramble(ctx, arg):
    if(arg == '3x3'):
        await ctx.send(scrambler333.get_WCA_scramble())
    elif(arg == '4x4'):
        await ctx.send(scrambler444.get_WCA_scramble())

@bot.command()
async def button(ctx):
    view = discord.ui.View()
    button = discord.ui.Button(label="click me")
    view.add_item(button)
    await ctx.send(view=view)


bot.run(os.getenv('TOKEN'))
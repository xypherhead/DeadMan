import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
load_dotenv()

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print("We have logged in as:", bot.user.name, '#', bot.user.discriminator)

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello mate!")

bot.run(getenv('TOKEN'))
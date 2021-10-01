import discord
from discord.ext import commands
# from discord.ext.commands.core import command

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print("We have logged in as:", bot.user.name, bot.user.avatar)

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello mate!")

bot.run('ODMyMzAyNDUzNTE2OTI2OTk3.YHh0EA.m14rpj80v7G0W7-7LKnXA9V78ls')
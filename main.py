import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
load_dotenv()

def DeadMan(file, data):
    if data == {}:
        courses = data['courses'] = []
    else:
        courses = data['courses']
    print(data)

    bot = commands.Bot(command_prefix='-')

    @bot.event
    async def on_ready():
        print("We have logged in as:", bot.user.name, '#', bot.user.discriminator)

    @bot.command()
    async def hello(ctx):
        await ctx.reply("Hello mate!")

    @bot.command(name='add')
    async def add_deadline(ctx, course:str = None, date:int = None, *, desc:str = None):
        if (course == None or date == None or desc == None):
            await ctx.reply("Usage: -add <Course Name> <Deadline Date in DDMM> <Deadline Description>")
            return
        try:
            if course not in courses:
                data[course] = {}
                data[course]['course_id'] = str(len(data['courses']))
                data[course]['count'] = 0
                data['courses'].append(course)

            deadline = {}
            deadline_ID = data[course]['course_id'] + str(data[course]['count'])
            deadline['Date'] = date
            deadline['Description'] = desc
            data[course][deadline_ID] = deadline

            data[course]['count'] += 1

            json_obj = json.dumps(data, indent = 4)
            # json.dump(data, file)

            with open(file, 'w') as f:
                f.write(json_obj)
                f.write('\n')
            
            await ctx.reply("Deadline Added!")

        except Exception as e:
            await ctx.reply(e)

    bot.run(getenv('TOKEN'))

def main():
    file = getenv('FILE')
    with open(file) as f:
        try:
            data = json.load(f)
        except:
            data = {}

    DeadMan(file, data)

if __name__ == "__main__":
    main()
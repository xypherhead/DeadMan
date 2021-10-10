import discord
import json
from discord.ext import commands
from discord.ext.commands.errors import BadArgument
from discord.ext.commands.help import MinimalHelpCommand
from dotenv import load_dotenv
from os import getenv
load_dotenv()

def DeadMan(file, data):
    if data == {}:
        courses = data['courses'] = []
    else:
        courses = data['courses']

    bot = commands.Bot(command_prefix='-', activity = discord.Activity(type = discord.ActivityType.custom) , status = discord.Status.idle, help_command=MinimalHelpCommand())

    @bot.event
    async def on_ready():
        print("We have logged in as:", bot.user.name, '#{}'.format(bot.user.discriminator))

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

    @add_deadline.error
    async def bad_argument(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Wrong argument passed!\nUsage: -add <Course Name> <Deadline Date in DDMM> <Deadline Description>")

    # @bot.command(name='courses')
    # async def list_courses(ctx):
    #     try:
    #         course_list = '**The courses added so far are:**\n>>> '
    #         for course in courses:
    #             course_list += course + '\n'
    #         await ctx.send(course_list)
    #     except Exception as e:
    #         await ctx.reply(e)

    @bot.command(name='listall')
    async def list_deadlines(ctx):
        try:
            all_list = '**Deadlines for all courses:**\n'
            for course in courses:
                course_list = '`{}:`\n'.format(course)
                for dl in data[course]:
                    if(dl == "course_id" or dl == "count"):
                        continue
                    else:
                        course_list += '> '
                        course_list += str(data[course][dl]["Date"] // 100) + '/' + (str(data[course][dl]["Date"] % 100))
                        course_list += ': ' + data[course][dl]["Description"] + '\n'
                all_list += course_list
            await ctx.send(all_list)
        except Exception as e:
            await ctx.reply(e)

    # @bot.command(name='help')
    # async def _help(ctx):
    #     pass

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
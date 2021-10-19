import discord
import json
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()

def DeadMan(file, data):

    bot = commands.Bot(command_prefix='-', activity = discord.Activity(type = discord.ActivityType.watching, name = "Deadlines!"))

    @bot.event
    async def on_ready():
        print("We have logged in as:", bot.user.name, '#{}'.format(bot.user.discriminator))

    # setting up empty database
    if data == {}:
        courses = data['courses'] = []
    else:
        courses = data['courses']

    @bot.command(description = "Replies the user with hello")
    async def hello(ctx):

        await ctx.reply("Hello mate!")

    @bot.command(name='add', description = "Adds a deadline.")
    async def add_deadline(ctx, course:str = None, ddmm_date:int = None, *, description:str = None):
        if (course == None or ddmm_date == None or description == None or len(str(ddmm_date)) != 4):
            await ctx.reply("Usage: -add <Course> <Deadline in DDMM> <Description>")
            return

        try:
            if course not in courses:
                data[course] = {}
                data[course]['course_id'] = str(len(data['courses']))
                data[course]['count'] = 0
                data['courses'].append(course)

            deadline = {}
            deadline_ID = data[course]['course_id'] + str(data[course]['count'])
            deadline['Date'] = ddmm_date
            deadline['Description'] = description
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
    async def _bad_argument(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Wrong argument passed!\nUsage: -add <Course> <Deadline in DDMM> <Description>")

    @bot.command(name='courses', description = "Lists all the courses for which deadlines have been added.")
    async def list_courses(ctx):
        try:
            course_list = discord.Embed(title = "All courses", description = "Listing all courses for which deadlines have been added", color = discord.Color.blue())
            for course in courses:
                course_list.add_field(name = f'{course}', value = f'{data[course]["count"]} deadlines', inline = False)
            await ctx.send(embed = course_list)

        except Exception as e:
            await ctx.reply(e)

    @bot.command(name='listall', description = "Lists all the deadlies that have been added so far")
    async def list_deadlines(ctx):
        try:
            all_list = discord.Embed(title = "All deadlines", description = "Listing all deadlines have been added", color = discord.Color.blue())
            for course in courses:
                course_list = ''
                counter = 0
                for dl in data[course]:
                    if(dl == "course_id" or dl == "count"):
                        continue
                    else:
                        counter += 1
                        course_list += f'{counter}. '
                        course_list += f'`{(data[course][dl]["Date"] // 100)}/{data[course][dl]["Date"] % 100}`'
                        course_list += f': {data[course][dl]["Description"]}\n'
                all_list.add_field(name = f'{course}', value = course_list, inline = False)
            await ctx.send(embed = all_list)

        except Exception as e:
            await ctx.reply(e)

    bot.run(os.getenv('TOKEN'))

def main():

    # using json file as temporary database
    file = os.getenv('FILE')
    with open(file) as f:
        try:
            data = json.load(f)
        except:
            data = {}

    DeadMan(file, data)

if __name__ == "__main__":
    main()
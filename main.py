import os
import json
import discord
import grading_system as gs
from discord.ext.commands import Bot
from termcolor import colored

bot = Bot(command_prefix='$', intents=discord.Intents.all())


@bot.event
async def on_ready():
    guild = await bot.fetch_guild(779290119738884108)   # used server
    members = await guild.fetch_members().flatten()     # gets the member list
    print('Starting to check the databases')

    with open('databases/social_credit.json', 'r+') as f:   # sets up the SC map database
        jsonObj = json.load(f)
        for member in members:
            if str(member.id) not in jsonObj.keys() and not member.bot:
                print(colored(f'[SC map]: New member detected: {member}', 'yellow'))
                jsonObj[str(member.id)] = 1000
        f.seek(0)
        json.dump(jsonObj, f, indent=4)

    with open('databases/ranks_rvrs.json', 'w') as f:
        jsonObj = gs.sorterRvrs(jsonObj)
        json.dump(jsonObj, f, indent=4)

    with open('databases/logs.json', 'r+') as f:    # sets up the logs database
        jsonObj = json.load(f)
        for member in members:
            if str(member.id) not in jsonObj.keys() and not member.bot:
                print(colored(f'[Logs]: New member detected: {member}', 'yellow'))
                jsonObj[str(member.id)] = {}
        f.seek(0)
        json.dump(jsonObj, f, indent=4)

    print(colored('Databases synced up and ready to go', 'green'))

    for file in os.listdir('Cogs'):     # loads the cogs
        if not file.endswith('.py'):
            continue
        try:
            bot.load_extension(f'Cogs.{file[:-3]}')
            print(colored(f'Loaded {file}', 'green'))
        except Exception as E:
            print(colored(f'Failed to Load {file}: {E}', 'red'))
    print('Finished loading cogs')

    print('Bot ready')


@bot.event
async def on_disconnect():
    print(colored('Disconnected', 'red'))

    @bot.event
    async def on_connect():     # smart shit which doesn't work
        print(colored('Reconnected', 'green'))


if __name__ == '__main__':
    bot.run('ODk2NzI3MTQ2MjQyOTIwNDk4.YWLUPA.Z4Cq4aOhjBC2RMoh-EWzYajhbf4')

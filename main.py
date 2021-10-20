import os
import json
import discord
import grading_system as gs
from discord.ext.commands import Bot

bot = Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    guild = await bot.fetch_guild(779290119738884108)   # used server
    members = await guild.fetch_members().flatten()     # gets the member list
    print('Starting to check the databases')

    with open('databases/social_credit.json', 'r+') as f:   # sets up the SC map database
        jsonObj = json.load(f)
        for member in members:
            if str(member.id) not in jsonObj.keys() and not member.bot:
                print(f'[SC map]: New member detected: {member}')
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
                print(f'[Logs]: New member detected: {member}')
                jsonObj[str(member.id)] = {}
        f.seek(0)
        json.dump(jsonObj, f, indent=4)

    print('Databases synced up and ready to go')

    for file in os.listdir('Cogs'):     # loads the cogs
        if not file.endswith('.py'):
            continue
        try:
            bot.load_extension(f'Cogs.{file[:-3]}')
            print(f'Loaded {file}')
        except Exception as E:
            print(f'Failed to Load {file}: {E}')
    print('Finished loading cogs')

    print('Bot ready')


@bot.event
async def on_disconnect():
    print('Disconnected')


if __name__ == '__main__':
    token = input('Enter the token: ')
    bot.run(token)

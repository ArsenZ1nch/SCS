import os
import json
import discord
from discord.ext.commands import Bot
from dpyConsole import Console
from termcolor import colored

bot = Bot(command_prefix='!', intents=discord.Intents.all())
console = Console(bot)


@bot.event
async def on_ready():
    guild = await bot.fetch_guild(896724049286295582)
    members = await guild.fetch_members().flatten()
    print('Starting to check the databases')
    
    with open('databases/social_credit.json', 'r+') as f:
        jsonObj = json.load(f)
        for member in members:
            if str(member.id) not in jsonObj.keys():
                print(colored(f'New member detected: {member}', 'yellow'))
                jsonObj[str(member.id)] = 1000
        f.seek(0)
        json.dump(jsonObj, f, indent=4)
    
    print(colored('Databases synced up and ready to go', 'green'))
    
    for file in os.listdir('Cogs'):
        if not file.endswith('.py'):
            continue
    
        try:
            bot.load_extension(f'Cogs.{file[:-3]}')
            print(colored(f'Loaded {file}', 'green'))
        except Exception as E:
            print(colored(f'Failed to Load {file}: {E}', 'red'))
    print('Finished')

    print('Bot ready')
    console.start()


@bot.event
async def on_disconnect():
    print(colored('Disconnected', 'red'))

    @bot.event
    async def on_connect():
        print(colored('Reconnected', 'green'))


@console.command()
async def dm(user: discord.User, msg):
    await user.send(f"{msg}")
    print(f"Sent message to {user.name}: '{msg}'")


@console.command()
async def loadCogs(*args):
    if args[0] == '-A':
        for file in os.listdir('Cogs'):
            if not file.endswith('.py'):
                continue

            try:
                bot.load_extension(f'Cogs.{file[:-3]}')
                print(colored(f'Loaded {file}', 'green'))
            except Exception as E:
                print(colored(f'Failed to load {file}: {E}', 'red'))
        return print('Finished')

    for file in args:
        try:
            bot.load_extension(f'Cogs.{file}')
            print(colored(f'Loaded {file}', 'green'))
        except Exception as E:
            print(E)
            print(colored(f'Failed to load {file}: {E}', 'red'))
    return print('Finished')


@console.command()
async def unloadCogs(*args):
    if args[0] == '-A':
        for file in os.listdir('Cogs'):
            if not file.endswith('.py'):
                continue

            try:
                bot.unload_extension(f'Cogs.{file[:-3]}')
                print(colored(f'Unloaded {file}', 'green'))
            except Exception as E:
                print(colored(f'Failed to unload {file}: {E}', 'red'))
        return print('Finished')

    for file in args:
        try:
            bot.unload_extension(f'Cogs.{file}')
            print(colored(f'Unloaded {file}', 'green'))
        except Exception as E:
            print(colored(f'Failed to unload {file}: {E}', 'red'))
    return print('Finished')


if __name__ == '__main__':
    bot.run('ODk2NzI3MTQ2MjQyOTIwNDk4.YWLUPA.Z4Cq4aOhjBC2RMoh-EWzYajhbf4')
    # bot.run('')

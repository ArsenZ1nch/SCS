import discord
from discord.ext.commands import Bot
from dpyConsole import Console
from termcolor import colored


bot = Bot(command_prefix="!", intents=discord.Intents.all())
console = Console(bot)


@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_disconnect():
    print(colored("Disconnected", "red"))

    @bot.event
    async def on_connect():
        print(colored("Reconnected", "green"))


@console.command()
async def dm(user: discord.User, msg):
    print(f"Sending message to {user.name}: '{msg}'")
    await user.send(f"{msg}")


if __name__ == '__main__':
    console.start()
    bot.run("ODk2NzI3MTQ2MjQyOTIwNDk4.YWLUPA.Z4Cq4aOhjBC2RMoh-EWzYajhbf4")

import discord
from discord.ext import commands
import json
import time

DATABASES = 'databases'
SC_MAP = 'social_credit.json'
LOGS = 'logs.json'


class ManCmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def promote(self, ctx, usr: discord.Member, sc: int, *, reason=None):
        if ctx.author.top_role < ctx.guild.get_role(896458600166330368):
            return await ctx.send('不')

        if ctx.author.top_role <= usr.top_role or sc == 0:
            return await ctx.send('不')

        if sc > 0:
            change = 'Promotion'
        else:
            change = 'Demotion'

        with open(f'{DATABASES}/{SC_MAP}', 'r+') as f:
            jsonObj = json.load(f)
            jsonObj[str(usr.id)] += sc
            f.seek(0)
            json.dump(jsonObj, f, indent=4)

        with open(f'{DATABASES}/{LOGS}', 'r+') as f:
            jsonObj = json.load(f)

            epoch = str(int(time.time()))
            jsonObj.update({
                str(usr.id):
                    {epoch: {
                        'Change': change,
                        'Change of social credit': sc
                    }}
            })
            if reason:
                jsonObj[str(usr.id)][epoch].update({'Reason': reason})

            f.seek(0)
            json.dump(jsonObj, f, indent=4)

        print('finished')


def setup(client):
    client.add_cog(ManCmds(client))

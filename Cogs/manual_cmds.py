import discord
from discord.ext import commands
import json
import time
import os
import grading_system as gs

DATABASES = 'databases'
SC_MAP = 'social_credit.json'
LOGS = 'logs.json'
RANKS, rRANKS = 'ranks.json', 'ranks_rvrs.json'


class ManCmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def promote(self, ctx, usr: discord.Member, sc: int, *, reason=None):
        if ctx.author.top_role < ctx.guild.get_role(896458600166330368) or sc == 0:      # checks if author is A+ or higher + if social credit is not 0
            return await ctx.send('不')

        if ctx.author.top_role <= usr.top_role and ctx.author != ctx.guild.owner:  # checks if author is higher in hierarchy than the target unless author is the owner
            return await ctx.send('不')

        if reason:
            if len(reason) > 69:
                reason = None
                await ctx.send('The reason is too long')

        if sc > 0:  # check if the social credit is demotion or promotion
            change = 'Promotion 🤝'
            rsn = f'`{reason}`' if reason else 'their excellent behaviour'
            msg = f'{usr} was awarded with {sc} social credit for {rsn} 🇨🇳 🤝'
        else:
            change = 'Demotion 🤬'
            rsn = f'`{reason}`' if reason else 'their atrocious anti-Chinese behaviour'
            msg = f'{usr} just lost {abs(sc)} social credit for {rsn} 😡 😡'

        '''
        Setting up the embed (2 more lines in the next big section)
        '''
        embed = discord.Embed(title=change, colour=discord.Color.from_rgb(226, 27, 35))
        embed.description = f'You have been {change[:-5].lower()}ed by the CCP!'
        embed.set_thumbnail(url='https://c.tenor.com/swKlGxmxsBwAAAAd/social-credit-denis-romavich.gif')
        embed.set_image(
            url='https://c.tenor.com/RvBPEdvCqHkAAAAC/social-credit.gif' if sc < 0 else 'https://i.ytimg.com/vi/pq-koFphG0k/maxresdefault.jpg')
        embed.add_field(name=f'Amount of {"lost" if sc < 0 else "gained"} credit:', value=str(abs(sc)))
        if reason:
            embed.add_field(name='Reason:', value=reason)
        embed.set_footer(text='你太无耻了！' if sc < 0 else '做得太好了！')
        '''
        %%%
        '''


        '''
        I/O work with databases
        '''
        print(f'Promoting {usr} by {sc} social credit')  # quick log

        id = str(usr.id)
        with open(f'{DATABASES}/{SC_MAP}', 'r') as f:  # modifying the map
            jsonObj = json.load(f)
            jsonObj[id] += sc
            embed.add_field(name='Current social score:', value=jsonObj[id], inline=False)  # for embed
        with open(f'{DATABASES}/{SC_MAP}', 'w') as f:
            json.dump(jsonObj, f, indent=4)

        with open(f'{DATABASES}/{rRANKS}', 'r') as f:  # modifying the grade map (confusing shit)
            jsonObj1 = json.load(f)
            grade = gs.check_grade(jsonObj[id])
            if grade != jsonObj1[id]:
                jsonObj1[id] = grade
                with open(f'{DATABASES}/{rRANKS}', 'w') as f:
                    json.dump(jsonObj1, f, indent=4)
            embed.add_field(name='Current rank:', value=grade, inline=False)  # for embed

        with open(f'{DATABASES}/{LOGS}', 'r') as f:  # modifying the logs
            jsonObj = json.load(f)

            epoch = str(int(time.time()))  # epoch is the key
            jsonObj[id].update({epoch: {
                'Change': change[:-2],
                'Change of social score': sc,
                'Author': ctx.author.id
            }}
            )
            if reason:
                jsonObj[id][epoch].update({'Reason': reason})
        with open(f'{DATABASES}/{LOGS}', 'w') as f:
            json.dump(jsonObj, f, indent=4)
        '''
        %%%
        '''


        await ctx.send(msg)  # sends message
        await usr.send(embed=embed)  # + embed


    @commands.command()
    async def score(self, ctx, usr: discord.User = None):
        if not usr:
            usr = ctx.author
        id = str(usr.id)

        '''
        JSON input block
        '''
        with open(f'{DATABASES}/{SC_MAP}', 'r') as f:
            sc_map = json.load(f)
        with open(f'{DATABASES}/{rRANKS}', 'r') as f:
            grade_map = json.load(f)
        with open(f'{DATABASES}/{LOGS}', 'r') as f:
            logs = json.load(f)
        '''
        %%%
        '''

        score, rank = sc_map[id], grade_map[id]    # making a few variables
        needed_sc = gs.needed_sc(score, rank)

        '''
        assigning the change value to a variable if usr was pro-/demoted
        '''
        try:
            array = list(logs[id].keys())   # makes a list of keys
            key = array[-1]    # assigns the most recent change key to a variable
            rec_change = logs[id][key]  # uses the variable to find the most recent change
        except Exception as E:
            print(E)
            rec_change = None
        '''
        %%%
        '''

        '''''''''
        constructing an embed
        '''''''''
        embed = discord.Embed(title=f"{usr}'s report", colour=discord.Color.from_rgb(226, 27, 35))
        embed.set_thumbnail(url='https://c.tenor.com/EQDejgLJD-YAAAAd/social-credit.gif')
        embed.set_image(url=usr.avatar_url)
        embed.add_field(name='Social score:', value=score)
        embed.add_field(name='Current rank:', value=rank)
        '''
        a bunch of confusing conditional blocks
        '''
        if needed_sc:
            embed.add_field(name=f'Social credit needed for the next rank ({needed_sc[1]}):', value=needed_sc[0], inline=False)
        if rec_change:
            sc_change = rec_change['Change of social score']
            num_change = f'+{sc_change}' if sc_change > 0 else sc_change
            change = f'{rec_change["Change"]} ({num_change} social credit)'
            embed.add_field(name='Most recent social score change:', value=change, inline=False)
        if score > 1001:    # 1001 = A+
            embed.set_footer(text='做得太好了！')    # --> eng: very well done
        '''''''''
        %%%%%%%%%
        '''''''''

        await ctx.send(embed=embed)

    @commands.command()
    async def send_file(self, ctx, *files):  # for manual sending of database files
        for file in files:
            await ctx.send(file=discord.File(f'databases/{file}.json'))

    @commands.command()
    async def send_all(self, ctx):  # for manual sending of all database files
        for file in os.listdir('databases'):
            await ctx.send(file=discord.File(f'databases/{file}'))


def setup(client):
    client.add_cog(ManCmds(client))

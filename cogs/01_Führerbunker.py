import discord
import json
import os
import asyncio
from discord.ext import commands, tasks
from datetime import datetime

path = os.path.dirname(os.path.realpath(__file__))

async def wakeup_loop(self, ctx, user, count):
    afk = ctx.author.voice.channel.guild.afk_channel
    wake_channel = ctx.guild.get_channel(772940637599301652)
    dest = ctx.author.voice.channel
    current_state = (f'{user.voice.self_deaf}',f'{user.voice.self_mute}')
    i = 0
    while i < count:
        i = i + 1
        if current_state != (f'{ctx.guild.get_member(user.id).voice.self_deaf}',f'{ctx.guild.get_member(user.id).voice.self_mute}'):
                await user.edit(voice_channel=dest)
                await ctx.channel.send(f'{user.mention} was awoken!')
                return
        try:
            await user.edit(voice_channel=wake_channel)
            await asyncio.sleep(1)
            await user.edit(voice_channel=afk)
            await asyncio.sleep(1)
        except:
            break
    await user.edit(voice_channel=dest)
    await ctx.channel.send(f'No response was triggered good luck!')

async def discord_tour(self, ctx, user):
    dest = ctx.author.voice.channel
    for channel in ctx.guild.voice_channels:
        await user.edit(voice_channel=channel)
        await asyncio.sleep(0.2)
        if ctx.guild.get_member(user.id).voice == None:
            return
    await user.edit(voice_channel=dest)

class Führerbunker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.unmute_hoizmeih.start()

    @commands.command(name='ttt', help='Sends Link to TTT Server')
    async def ttt(self, ctx):
        if ctx.author == self.bot.user or ctx.guild == None:
            return
        embedTTT = discord.Embed(
            title=f'<:TTT:769985066611769394><:TTT:769985066611769394><:TTT:769985066611769394> Server',
            url="http://85.214.63.77:8080/ttt",
            color=15746887)
        embedTTT.add_field(name='Join', value='[Join\nHERE!](http://85.214.63.77:8080/ttt)')
        embedTTT.add_field(name='Mod Collection', value='[Subscribe\nHERE!](https://steamcommunity.com/sharedfiles/filedetails/?id=2022328842)')
        embedTTT.set_thumbnail(url='https://maurits.tv/data/garrysmod/wiki/wiki.garrysmod.com/images/5/5d/EX_GMOD12_ttt_logo_cropped.png')

        await ctx.send(embed=embedTTT)
        return

    @commands.command(name='frieden',aliases=['friedenstreppe'],brief='Start Friedenstreppe', help='Move both mentioned members to Friedenstreppe Voice Channel\ncooldown= 2 uses per 300sec')
    @commands.cooldown(1,300,type=commands.BucketType.user)
    async def frieden(self, ctx, user1 : discord.Member, user2 : discord.Member ):
        if user1.voice == None or user2.voice == None:
            await ctx.channel.send(f'both users need to be connected to voice!')
            return
        await user1.edit(voice_channel=self.bot.get_channel(772079329819623445))
        await user2.edit(voice_channel=self.bot.get_channel(772079329819623445))
        return

    @commands.command(name='HoizMeih', aliases=['hm'], brief='Mute Member for 30sec', help='Mute Member because he smells bad LOL\nCooldown= 2 uses per 120sec')
    @commands.cooldown(2,120,type=commands.BucketType.user)
    async def HoizMeih(self, ctx, user : discord.Member):
        if ctx.author == self.bot.user or ctx.guild == None:
            return
        if user.voice == None:
            await ctx.channel.send(f'user not connected to voice')
            ctx.command.reset_cooldown(ctx)
            return
        await user.edit(mute=True)
        await ctx.channel.send(f'A ruah is jetzt amoi!\n{user.mention} was muted for 30sec')

        with open (f'{path}/../json/hoizmeih.json', 'r') as f:
            muted = json.load(f)
        with open (f'{path}/../json/hoizmeih.json', 'w') as f:
            to_mute = {
            'id' : f'{str(user.id)}',
            'guild': f'{str(ctx.guild.id)}',
            'timestamp': f'{str(datetime.now().timestamp())}'
            }
            muted[f'{user}'] = to_mute

            json.dump(muted, f, indent=4)
        return

    @commands.command(name='wakeup',aliases=['wake'],brief='Try to wake user from mute xD',help='Moves Called member between afk and your Voice Channel like x number of times def is 5 \nonly works if user is connected to a Voice Channel\ncooldown=2 uses per 300sec')
    @commands.cooldown(2,120,type=commands.BucketType.user)
    async def wakeup(self,ctx, user : discord.Member, count : int  = 3):
            if count > 100:
                count = 3
                await ctx.channel.send(f'requested count exceeds max amount')
                ctx.command.reset_cooldown(ctx)
                return
            if ctx.author.voice == None or user.voice == None:
                await ctx.channel.send(f'both users need to be connected to voice ')
                ctx.command.reset_cooldown(ctx)
                return
            if user.voice.channel == ctx.guild.afk_channel or user.voice.afk == True or (user.voice.self_deaf == True and user.voice.self_mute == True):
                self.bot.loop.create_task(wakeup_loop(self,ctx,user,count))
            else:
                await ctx.channel.send(f'User voice not in right state\naka. Abuse Protection')
            return


    @commands.command(name='tour',help='show the whole discord to user with a short break',brief='Short discord Tour w break')
    @commands.cooldown(1,300,type=commands.BucketType.guild)
    async def Tour(self, ctx, user : discord.Member):
        if user.voice == None or ctx.author.voice == None:
            ctx.command.reset_cooldown(ctx)
            await ctx.channel.send(f'both users need to be connected to voice')
            return
        self.bot.loop.create_task(discord_tour(self, ctx, user))
        return


    @tasks.loop(seconds=10)
    async def unmute_hoizmeih(self):
        if self.bot._ready._value == False:
            return
        with open (f'{path}/../json/hoizmeih.json', 'r') as f:
            content = json.load(f)
        for entry in list(content):
            user = content[str(entry)]
            if (datetime.now().timestamp() -30) >= float(user['timestamp']):
                member = self.bot.get_guild(int(user['guild'])).get_member(int(user['id']))
                try:
                    await member.edit(mute=False)
                except:
                    print('member not connected to voice')
                    continue
                #Pop entry from File
                with open (f'{path}/../json/hoizmeih.json', 'w') as f:
                    content.pop(str(entry))
                    json.dump(content, f, indent=4)

def setup(bot):
    bot.add_cog(Führerbunker(bot))
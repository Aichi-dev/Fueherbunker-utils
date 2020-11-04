import discord
from discord.ext import commands

# This File does nothing only for help LOL

class Among_Us(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='among', brief='Start AmongUs game', help='Moves all members to AmongUs Channel')
    async def among(self, ctx):
        if ctx.author == self.bot.user or ctx.guild == None:
            return
        try:
            ids = list(ctx.channel.guild._voice_states.keys())
            for id in ids:
                member = ctx.guild.get_member(int(id))
                await member.edit(voice_channel=self.bot.get_channel(759394678939713606))
        except:
            await ctx.channel.send('Something went wrong')
            return
        return

    @commands.command(name='amongmute', brief='Bot only! Mute channel members', help='BOT / WebH ONLY! Mute all members in provided ChannelID')
    async def amongmute(self, ctx):
        pass
    @commands.command(name='amongunmute', brief='Bot only! Unmute channel members', help='BOT / WebH ONLY! Unmute all members which were muted while in provided ChannelID')
    async def amongunmute(self, ctx):
        pass
    @commands.command(name='amongclear', brief='Unmute all members of Guild', help='Unmute all muted members in current Guild if connected to voice')
    async def amongclear(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Among_Us(bot))
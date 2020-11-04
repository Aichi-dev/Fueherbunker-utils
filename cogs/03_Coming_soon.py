import discord
import json
import os
import asyncio
from discord.ext import commands, tasks
from datetime import datetime


path = os.path.dirname(os.path.realpath(__file__))

async def discord_tour(self, ctx, user):
    dest = ctx.author.voice.channel
    for channel in ctx.guild.voice_channels:
        await user.edit(voice_channel=channel)
        if ctx.guild.get_member(user.id).voice == None:
            await asyncio.sleep(0.5)
    await user.edit(voice_channel=dest)

class coming_soon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='Suggestions_plz', help='in desperate need :)')
    async def Suggestions_plz(self, ctx):
        if ctx.author == self.bot.user or ctx.guild == None:
            return

    @commands.command(name='tour',help='show the whole discord to user',brief='Short discord Tour')
    @commands.cooldown(1,300,type=commands.BucketType.guild)
    async def Tour(self, ctx, user : discord.Member):
        if user.voice == None or ctx.author.voice == None:
            ctx.command.reset_cooldown(ctx)
            await ctx.channel.send(f'both users need to be connected to voice')
            return
        self.bot.loop.create_task(discord_tour(self, ctx, user))
        return




def setup(bot):
    bot.add_cog(coming_soon(bot))
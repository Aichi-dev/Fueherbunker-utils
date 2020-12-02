import discord
import json
import os
import asyncio
from discord.ext import commands, tasks
from datetime import datetime


path = os.path.dirname(os.path.realpath(__file__))



class coming_soon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Suggestions_plz', help='in desperate need :)')
    async def Suggestions_plz(self, ctx):
        if ctx.author == self.bot.user or ctx.guild == None:
            return
    @commands.command(name='Music_Bot', help='HELL YEAH. w. YouTube')
    async def Music_Bot(self, ctx):
        if ctx.author == self.bot.user or ctx.guild == None:
            return





def setup(bot):
    bot.add_cog(coming_soon(bot))
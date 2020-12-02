import discord
import json
import os
import asyncio
import youtube_dl
from discord.utils import get
from discord.ext import commands, tasks
from datetime import datetime


path = os.path.dirname(os.path.realpath(__file__))

async def loop_sound(self,ctx,voice,audio):
    voice = get(self.bot.voice_clients, guild=ctx.guild)
    def repeat(voice, audio):
        try:
            voice.play(discord.FFmpegPCMAudio(audio), after=lambda e: repeat(voice, audio))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
        except:
            pass
    if voice:
        voice.play(discord.FFmpegPCMAudio(audio), after=lambda e: repeat(voice, audio))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07


class Music_Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

####
    @commands.command(name='play',help='Play YoutTube Video (Audio Only)',brief='MusicBot Youtube Link')
    async def play(self, ctx, url: str, loop : bool=False):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        song_there = os.path.isfile(f"{path}/../sounds/ydl/song.mp3")
        try:
            if voice.is_playing():
                voice.stop()
                await asyncio.sleep(1)
            if song_there:
                os.remove(f"{path}/../sounds/ydl/song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        #await ctx.send("Getting everything ready now")

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path}/../sounds/ydl/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir(f"{path}/../sounds/ydl/"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(f"{path}/../sounds/ydl/{name}", f"{path}/../sounds/ydl/song.mp3")

        audio = f"{path}/../sounds/ydl/song.mp3"
        nname = name.rsplit("-", 2)
        if loop == False:
            voice.play(discord.FFmpegPCMAudio(audio))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            await ctx.send(f"Playing: {nname[0]}")
            self.stop_if_not_playing.start(ctx)
        else:
            await ctx.send(f"Looping: {nname[0]}")
            await loop_sound(self,ctx,voice,audio)

        print("playing\n")


    @commands.command(name='stop',help='Stop Music',brief='just STAP IT')
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            if voice.is_playing():
                voice.stop()
                await voice.disconnect()
                self.stop_if_not_playing.stop()
            else:
                await voice.disconnect()
                self.stop_if_not_playing.stop()
                return
        else:
            await ctx.channel.send(f'Dafuq should i stop if i am NOT PLAYING ANYTHING YOU FOOL!')

    @commands.command(name='volume_up',help='increase volume',brief='increase volume')
    async def volume_up(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.source.volume = voice.source.volume + 0.1
        else:
            return

    @commands.command(name='volume_down',help='decrase volume',brief='decrase volume')
    async def volume_down(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.source.volume = voice.source.volume - 0.1
        else:
            return
    @tasks.loop(seconds=10)
    async def stop_if_not_playing(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            pass
        elif not voice:
            self.stop_if_not_playing.stop()
            return
        else:
            self.stop_if_not_playing.stop()






def setup(bot):
    bot.add_cog(Music_Voice(bot))
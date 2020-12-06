import discord
import json
import os
import asyncio
import youtube_dl
import random
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
    @commands.command(name='play',help='Play YoutTube Video (Audio Only)\nPass True after url to loop infinitley',brief='MusicBot Youtube Link')
    async def play(self, ctx, url: str, loop : bool=False):
        if self.stop_if_not_playing.is_running():
            self.stop_if_not_playing.cancel()
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
                self.stop_if_not_playing.cancel()
            else:
                await voice.disconnect()
                self.stop_if_not_playing.cancel()
                return
        else:
            await ctx.channel.send(f'Dafuq should i stop if i am NOT PLAYING ANYTHING YOU FOOL!')

    @commands.command(name='volume_up',help='increase volume',brief='increase volume')
    async def volume_up(self, ctx, amount : int = 0.1):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.source.volume = voice.source.volume + amount
        else:
            return

    @commands.command(name='volume_down',help='decrase volume',brief='decrase volume')
    async def volume_down(self, ctx, amount : int = 0.1):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.source.volume = voice.source.volume - amount
        else:
            return

    @commands.command(name='sound',help='Play soundfile!',brief='Play sound <name>!')
    async def sound(self, ctx, name : str = "random"):

        files = [f for f in os.listdir(f"{path}/../sounds/") if f.endswith(".mp3")]
        play = None

        if name == "random":
            play = random.choice(files)
        else:
            for filename in files:
                if filename.endswith('.mp3') and filename.startswith(f'{name}'):
                    play = filename
        if play is None:
            return
        else:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            if voice.is_playing():
                voice.stop()
                await asyncio.sleep(1)
            voice.play(discord.FFmpegPCMAudio(f"{path}/../sounds/{play}"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            await ctx.send(f"Playing: {play}")
            if self.stop_if_not_playing.is_running():
                self.stop_if_not_playing.cancel()
            self.stop_if_not_playing.start(ctx)

    @commands.command(name='soundlist',help='Get list of all available sounds',brief='list of available sounds')
    async def soundlist(self, ctx):
        files = [f for f in os.listdir(f"{path}/../sounds/") if f.endswith(".mp3")]
        embed=discord.Embed(title="Sound Files", description="to play a file send the fbsound FILENAME \nexample: fbsound gaunzn")
        for f in files:
            embed.add_field(name= "Sound:", value = f'{f}', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='soundadd',help='Upload mp3 as attachment!',brief='Add mp3 sound!')
    async def soundadd(self, ctx, *args):
        if len(ctx.message.attachments) > 0:
            if not ctx.message.attachments[0].filename.endswith(".mp3"):
                await ctx.channel.send("File must be .mp3!")
                return
            mp3_file_name = ctx.message.attachments[0].filename.lower().replace(" ", "_")
            mp3_file_path = f'{path}/../sounds/{mp3_file_name}'
            await ctx.message.attachments[0].save(mp3_file_path)
            await ctx.channel.send(f'Sound {mp3_file_name} added successfully!')


    @tasks.loop(seconds=10)
    async def stop_if_not_playing(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if voice and voice.is_playing():
                pass
            elif not voice:
                self.stop_if_not_playing.stop()
                return
            else:
                await voice.disconnect()
                self.stop_if_not_playing.stop()
        except:
            return


def setup(bot):
    bot.add_cog(Music_Voice(bot))
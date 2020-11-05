# bot.py
import os
import discord
import json
from discord.ext import commands
from discord.ext import tasks

from dotenv import load_dotenv
from datetime import datetime

path = os.path.dirname(os.path.realpath(__file__))

if os.path.exists(f'{path}/json/admins.json'):
    with open (f'{path}/json/admins.json', 'r') as f:
        admins = json.load(f)
        f.close()
else:
    with open (f'{path}/json/admins.json', 'w') as f:
        f.write('[]')
        f.close()
    with open (f'{path}/json/admins.json', 'r') as f:
        admins = json.load(f)
        f.close()


load_dotenv()

#TOKEN = os.getenv('TEST_DISCORD_TOKEN') #Test
TOKEN = os.getenv('PROD_DISCORD_TOKEN') #Prod


intents = discord.Intents.default()
intents.members = True
intents.bans = True

bot = commands.Bot(command_prefix='fb', intents=intents,case_insensitive=True)

@bot.event
async def on_ready():
    print(f'{bot.user.name} IS AM START!')
    await bot.change_presence(activity=discord.Game('w PP | fbhelp'))

@bot.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id not in admins:
        return
    for filename in os.listdir(f'{path}/cogs'):
        if filename.endswith('.py') and filename.startswith(f'{extension}'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    return

@bot.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id not in admins:
        return
    for filename in os.listdir(f'{path}/cogs'):
        if filename.endswith('.py') and filename.startswith(f'{extension}'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
    return

@bot.command(hidden=True)
async def reload(ctx, extension):
    if ctx.author.id not in admins:
        return
    for filename in os.listdir(f'{path}/cogs'):
        if filename.endswith('.py') and filename.startswith(f'{extension}'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')
    return

@bot.command(hidden=True)
async def promote(ctx, user : discord.Member):
    global admins
    if ctx.author.id not in admins:
        return
    if user.id in admins:
        await ctx.channel.send(f'User already admin!')
        return
    with open (f'{path}/json/admins.json', 'w') as f:
        admins.append(user.id)
        json.dump(admins, f)
        f.close()
    with open (f'{path}/json/admins.json', 'r') as f:
        admins = json.load(f)
        f.close()

@bot.command(hidden=True)
async def demote(ctx, user : discord.Member):
    global admins
    if ctx.author.id not in admins or user.id == 356861941182103552:
        return
    if user.id not in admins:
        await ctx.channel.send(f'User is not admin!')
        return
    with open (f'{path}/json/admins.json', 'w') as f:
        admins.remove(user.id)
        json.dump(admins, f)
        f.close()
    with open (f'{path}/json/admins.json', 'r') as f:
        admins = json.load(f)
        f.close()

@bot.command(hidden=True)
async def show_admins(ctx):
    names = []
    for a in admins:
        names.append(f'{ctx.guild.get_member(a).display_name}#{ctx.guild.get_member(a).discriminator}')
    await ctx.channel.send(f'Current admins: {names}')

# Webhook Commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild == None and message.author != bot.user:
        print(f'{(datetime.now()).strftime("%d/%m/%Y %H:%M:%S")} New Message from {message.author} in DMs\n{message.content} ')
        return
    if message.channel == message.guild.text_channels[0]:
        return

# Among Us Webhook Commands
    if 'Among_Us' in bot.cogs.keys():
        if message.content.startswith('amongmute ') or message.content.startswith('fbamongmute '):
            if message.author == bot.user or message.guild == None : #or message.author.bot == False
                return
            print(f'{message.content}') # debug
            #try to get channel
            try:
                voice_channel_id= int(message.content.split()[1])
                voice_channel = message.guild.get_channel(voice_channel_id)
                ids = list(voice_channel.voice_states.keys())
            except Exception:
                await message.channel.send(f'Please enter a Valid ID!')
                return
            if len(ids) >= 1:
                with open(f'{path}/channels/{voice_channel_id}_{message.guild.id}','a') as fh:
                    for id in ids:
                        fh.write('%s\n' % id)
                    fh.close()
                for id in ids:
                    member = message.guild.get_member(int(id))
                    print(member)
                    await member.edit(mute = True)
                return

        if message.content.startswith('amongunmute ') or message.content.startswith('fbamongunmute '):
            if message.author == bot.user or message.guild == None : #or message.author.bot == False
                return
            try:
                voice_channel_id= int(message.content.split()[1])
            except Exception:
                await message.channel.send(f'Please enter a Valid ID!')
                return
            #Read File with memberIDs
            if not os.path.exists(f'{path}/channels/{voice_channel_id}_{message.guild.id}'):
                print('no members were Muted in channel')
                return
            ids=[]
            try:
                with open(f'{path}/channels/{voice_channel_id}_{message.guild.id}','r') as fh:
                    for line in fh:
                        # remove linebreak which is the last character of the string
                        currentPlace = line[:-1]
                        if currentPlace not in ids:
                            # add item to the list
                            ids.append(currentPlace)
                    print(ids)
                    fh.close()
            except Exception:
                print('Error Reading File')
                return
            for id in ids:
                member = message.guild.get_member(int(id))
                await member.edit(mute = False)
            os.remove(f'{path}/channels/{voice_channel_id}_{message.guild.id}')

        if message.content.startswith('amongclear') or message.content.startswith('fbamongclear'):
            if message.author == bot.user or message.guild == None or message.author.bot == True:
                return
            try:
                for member in message.guild.members:
                    if member.voice != None and member.voice.mute == True:
                        await member.edit(mute = False)
                for filename in os.listdir(f'{path}/channels'):
                    if filename.endswith(f'{message.guild.id}'):
                        os.remove(f'{path}/channels/{filename}')
            except:
                print('error')
            return
# End Amon Us Webhook Commands

    await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
    try:
        await member.guild.fetch_ban(member)
        return
    except discord.NotFound:
        await member.guild.text_channels[0].send(f'{member.display_name}#{member.discriminator}  left the BUNKER')
    pass

@bot.event
async def on_member_ban(guild, user):
    await guild.text_channels[0].send(f'<:MARTIN:357915375436038154> {user.display_name}#{user.discriminator} <:gehdeeischern:378306434896625674> ||(User was Banned)||')
    pass



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if ctx.author.id in admins:
            await ctx.command.reinvoke(ctx)
        else:
            await ctx.channel.send(f'You are on Cooldown, try again later :D')
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.channel.send(f'Missing argument(s)! Command expects:\n{ctx.bot.command_prefix}{ctx.invoked_with} {ctx.command.signature}')
    elif isinstance(error,commands.MemberNotFound):
        await ctx.channel.send(f'Tag a valid member!')
    else:
        await bot.get_user(356861941182103552).send(f'Unhandled error:{type(error)}\n{error.args[0]}\n\ntriggerd_by:\n{ctx.author}\n\nmessage:\n{ctx.message.content}')
        raise error

for filename in os.listdir(f'{path}/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)

import psutil
import discord
import sys
import time
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
import utilities as util
# from tools import checkIfProcessRunning, randomNegativeEmoji, randomPositiveEmoji, getCurrentPlexStreams, getToken

# globals
PLEX_STATUS = ""

# get an instance of the client
client = commands.Bot(command_prefix = '.', help_command=None)

# get the discord token for running the client
TOKEN = util.getToken("C:\\discord-bot\\plexed-token.txt", "r")

# Tautulli stuff
TAUTULLI_SERVER = "localhost"
TAUTULLI_PORT = "8181"
TAUTULLI_APIKEY = util.getToken("C:\\tautulli-key\\apikey.txt", "r")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you watch Plex | .help'))
    updateStatus.start()
    print('Bot is ready.')

@client.command(aliases=['ram','cpu','serverload'])
async def load(ctx):
    # get the cpu usage
    cpu = util.getCPU()
    # get the ram as a percentage used
    ram = util.getRAM()
    # build response string
    response = "```Plex Server Load: \n" + \
                f"CPU: {cpu}%\n" + \
                f"RAM: {ram}%\n```"
    # reply with response
    await ctx.send(response)

@client.command(aliases=['heartbeat'])
async def status(ctx):
    await ctx.send(util.getStatus(TAUTULLI_SERVER, TAUTULLI_PORT, TAUTULLI_APIKEY))

@client.command()
async def streams(ctx):
    response = util.getCurrentPlexStreams(TAUTULLI_SERVER, TAUTULLI_PORT, TAUTULLI_APIKEY, False)
    await ctx.send(response)

@client.command()
async def help(ctx):
    response =  "```" + \
                ".help    : displays this message\n" + \
                ".load    : displays the RAM and CPU usage on the server" + \
                ".streams : displays how many active streams are running"
                ".status  : displays if the server is running as well as .load and .streams"
                "```"
    await ctx.send(response)

@tasks.loop(minutes=5.0)
async def updateStatus():
    global PLEX_STATUS

    # get the channel that we want to send this message in
    channel = get(client.get_all_channels(), name='status', type=discord.ChannelType.text)
    
    # get the server status
    response = util.getStatus(TAUTULLI_SERVER, TAUTULLI_PORT, TAUTULLI_APIKEY)
    response = response + "(I auto update every 10 min)"

    # check if this is our first time doing this or just an update
    if PLEX_STATUS == "":
        # first time
        PLEX_STATUS = await channel.send(response)
    else:
        # delete previous message and repost
        await PLEX_STATUS.delete()
        PLEX_STATUS = await channel.send(response)

# run the bot
client.run(TOKEN)


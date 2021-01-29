import psutil
import discord
import sys
import time
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
import utilities as util
from tautulli import Tautulli as tau

# get an instance of the client
CLIENT = commands.Bot(command_prefix = '.', help_command=None)

# globals
PLEX_STATUS = ""
PROCESSING_MSG = ""
PLEXED_TOKEN_FILE = "C:\\discord-bot\\plexed-token.txt"
PLEXED_BOT_TOKEN = util.getToken(PLEXED_TOKEN_FILE, "r")
TAUTULLI_API_FILE = "C:\\tautulli-key\\apikey.txt"
TAUTULLI_API_KEY = util.getToken(TAUTULLI_API_FILE, "r")

# Tautulli stuff
TAU = tau("localhost", "8181", TAUTULLI_API_KEY )

@CLIENT.event
async def on_ready():
    await CLIENT.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you watch Plex | .help'))
    updateStatus.start()
    print('Bot is ready.')

@CLIENT.command(aliases=['ram','cpu','serverload','usage'])
async def load(ctx):
    cpu = util.getCPU()
    ram = util.getRAM()
    # build response string
    response = "```Plex Server Load: \n" + \
                f"CPU: {cpu}%\n" + \
                f"RAM: {ram}%\n```"
    # reply with response
    await ctx.send(response)

@CLIENT.command(aliases=['heartbeat'])
async def status(ctx):
    processing = util.getProcessingMessage()
    PROCESSING_MSG = await ctx.send(processing)
    status = TAU.getStatus()
    await PROCESSING_MSG.delete()
    await ctx.send(status)

@CLIENT.command(aliases=['streaming'])
async def streams(ctx):
    processing = util.getProcessingMessage()
    PROCESSING_MSG = await ctx.send(processing)
    response = TAU.getCurrentPlexStreams(False)
    await PROCESSING_MSG.delete()
    await ctx.send(response)

@CLIENT.command()
async def help(ctx):
    response =  "```" + \
                ".help    : displays this message\n" + \
                ".load    : displays the RAM and CPU usage on the server\n" + \
                ".streams : displays how many active streams are running\n" + \
                ".status  : displays if the server is running as well as .load and .streams\n" + \
                "```"
    await ctx.send(response)

@tasks.loop(minutes=5.0)
async def updateStatus():
    global PLEX_STATUS

    # get the channel that we want to send this message in
    channel = get(CLIENT.get_all_channels(), name='status', type=discord.ChannelType.text)
    
    # delete the previous message and replace it
    if PLEX_STATUS != "":
        await PLEX_STATUS.delete()

    # get the processing placeholder cause hitting the APIs is a bit slow
    processing = util.getProcessingMessage()
    PROCESSING_MSG = await channel.send(processing)

    # get the server status
    response = TAU.getStatus()
    response = response + "\n(I auto update every 5 min)"

    # delete the processing message
    await PROCESSING_MSG.delete() 

    # send our new status
    PLEX_STATUS = await channel.send(response)



# run the bot
CLIENT.run(PLEXED_BOT_TOKEN)


import psutil
import discord
import sys
import time
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
from tools import checkIfProcessRunning
from tools import randomNegativeEmoji
from tools import randomPositiveEmoji

# globals
PLEX_STATUS = ""

client = commands.Bot(command_prefix = '.', help_command=None)

# get the discord token for running the client bot
f = open("C:\\discord-bot\\plexed-token.txt", "r")
TOKEN = f.read()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you watch Plex | .help'))
    updateStatus.start()
    print('Bot is ready.')

@client.command(aliases=['ram','cpu','serverload'])
async def load(ctx):
    # get the cpu usage
    cpu = psutil.cpu_percent()
    # get the ram as a percentage used
    ram = psutil.virtual_memory().percent
    # build response string
    response =  "```" + \
                "Plex Server Load: \n" + \
                "CPU: " + str(cpu) + "%\n" + \
                "RAM: " + str(ram) + "%\n" + \
                "```"
    # reply with response
    await ctx.send(response)

@client.command(aliases=['heartbeat'])
async def status(ctx):
    channel = get(client.get_all_channels(), name='status', type=discord.ChannelType.text)
    if checkIfProcessRunning("Plex Media Server"):
        response =  "Plex Status: \n" + \
                    'Running ' + randomPositiveEmoji()
    else:
        response =  "Plex Status: \n" + \
                    'Unknown ' + randomNegativeEmoji()

    PLEX_STATUS = await channel.send(response)

@client.command()
async def help(ctx):
    response =  "```" + \
                ".help : display this message\n" + \
                ".load : displays the RAM and CPU usage on the server" + \
                "```"
    await ctx.send(response)

@tasks.loop(minutes=10)
async def updateStatus():
    global PLEX_STATUS
    # check if Plex is running
    if checkIfProcessRunning("Plex Media Server"):
        response =  "Plex Status: \n" + \
                    'Running ' + randomPositiveEmoji()
    else:
        response =  "Plex Status: \n" + \
                    'Unknown ' + randomNegativeEmoji()

    # check if this is our first time doing this or just an update
    if PLEX_STATUS == "":
        # first time
        channel = get(client.get_all_channels(), name='status', type=discord.ChannelType.text)
        PLEX_STATUS = await channel.send(response)
    else:
        # update
        await PLEX_STATUS.edit(content=response)


client.run(TOKEN)


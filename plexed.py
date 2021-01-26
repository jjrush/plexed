import psutil
import discord
import sys
from discord.ext import commands

client = commands.Bot(command_prefix = '.', help_command=None)

# get the discord token for running the client bot
f = open("C:\\discord-bot\\plexed-token.txt", "r")
discordToken = f.read()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you watch Plex | .help'))
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

@client.command()
async def help(ctx):
    response =  "```" + \
                ".help : display this message\n" + \
                ".load : displays the RAM and CPU usage on the server" + \
                "```"
    await ctx.send(response)

client.run(discordToken)
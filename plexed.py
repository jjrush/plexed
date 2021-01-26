import psutil
import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command(aliases=['ram','load','serverload'])
async def cpu(ctx):
    # get the cpu usage
    cpu = psutil.cpu_percent()
    # get the ram as a percentage used
    ram = psutil.virtual_memory().percent
    # build response string
    response = "Plex Server Load: " + "\n" + "CPU: " + str(cpu) + "%" + "\n" + "RAM: " + str(ram) + "%"
    # reply with response
    await ctx.send(response)

client.run('ODAzMzc5ODA3MjY5NTUyMTc5.YA87wA.JjSlH83ZmaMUVjqujFl9h5E62hQ')
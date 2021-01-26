import psutil
import random
import requests
from datetime import datetime

def getRandomNum(limit):
    return random.randint(0,limit)

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def randomPositiveEmoji():
    emoji = ['<a:wobble:762882376279654411>',
        '<a:pepe_jedi:772037678098022420>',
        '<:pepe_love:762882214950076416>',
        '<a:too_groovy:781735199633309727>',
        '<a:yeet:767921785113935893>',
        '<:snugg_life:762882326530621442>',
        '<a:pepe_jammies:762882195953287188>',
        '<a:heart_bounce:774137053930848317>',
        ':white_check_mark:',
        '<a:peepo_comfy:762882124469633074>'
        
    ]
    return emoji[getRandomNum(len(emoji)-1)]

def randomNegativeEmoji():
    emoji = ['<:sus_eyes:762882349598769192>',
        '<:pepe_rage:772046857072672768>',
        '<:intensify:769314091180359760>',
        '<:ohno:762882047198494761>',
        '<a:pepe_cry2:781721318781091927>',
        '<:blob_think:767922392109416460>',
        ':skull:'

    ]
    return emoji[getRandomNum(len(emoji)-1)]

def getToken(f, t):
    f = open(f, t)
    return f.read()

def getCurrentPlexStreams(server, port, key, status):
    response = requests.get(f"http://{server}:{port}/api/v2?apikey={key}&cmd=get_activity").json()
    stream_count = response['response']['data']['stream_count']
    quote = "```"
    if status == True:
        quote = ""
    reply = f"{quote}There are currently {stream_count} active streams{quote}"
    return reply

def getRAM():
    return psutil.virtual_memory().percent

def getCPU():
    return psutil.cpu_percent()

def getStatus(server, port, key):
    response = "Plex Status: \n"
    # check if Plex is running
    if checkIfProcessRunning("Plex Media Server"):
        # build our response
        response = response + f'Running {randomPositiveEmoji()}\n'
    else:
        response = response + f'Unknown {randomNegativeEmoji()}\n'

    # get the number of streams
    response = response + getCurrentPlexStreams(server, port, key, True)
    # get the cpu usage
    cpu = getCPU()
    # get the ram as a percentage used
    ram = getRAM()
    # build response string
    response = response + \
                "\nPlex Server Load: \n" + \
                f"CPU: {cpu}%\n" + \
                f"RAM: {ram}%\n"
    return response
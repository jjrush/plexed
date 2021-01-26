import psutil
import random

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
        '<:snugg_life:762882326530621442>'
    ]
    return emoji[getRandomNum(len(emoji)-1)]

def randomNegativeEmoji():
    emoji = ['<:sus_eyes:762882349598769192>',
        '<:pepe_rage:772046857072672768>',
        '<:intensify:769314091180359760>',
        '<:ohno:762882047198494761>',
        '<a:pepe_cry2:781721318781091927>',
        '<:blob_think:767922392109416460>'
    ]
    return emoji[getRandomNum(len(emoji)-1)]

# def getRandomEmoji():


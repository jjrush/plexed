from tautulli import Tautulli as tau
import json
import requests
import utilities as util

TAUTULLI_API_FILE = "C:\\tautulli-key\\apikey.txt"
TAUTULLI_API_KEY = util.getToken(TAUTULLI_API_FILE, "r")

# get instance of tautulli class
TAU = tau("localhost", "8181", TAUTULLI_API_KEY)

print(TAU.getStatus())

    
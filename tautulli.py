import utilities as util
import requests
import json

class Tautulli():
    def __init__(self, server, port, key, status="Online"):
        self.server = server
        self.port = port
        self.key = key
        self.status = status

    def getCurrentPlexStreamsNumber(self):
        cmd = "get_activity"
        response = requests.get(f"http://{self.server}:{self.port}/api/v2?apikey={self.key}&cmd={cmd}").json()
        return int(response['response']['data']['stream_count'])


    def getCurrentPlexStreams(self, status):
        stream_count = self.getCurrentPlexStreamsNumber()
        quote = "```"
        titles = ""
        reply = ""
        if status == True:
            quote = ""
        else:
            if( self.getCurrentPlexStreamsNumber() > 0 ):
                titles = self.getCurrentlyStreamingTitles()
        reply = f"{quote}There are currently {stream_count} active streams:\n"
        reply = f"{reply}{titles}{quote}"
        return reply

    def getStatus(self):
        response = "Plex Status: \n"
        # check if Plex is running
        if util.checkIfProcessRunning("Plex Media Server"):
            # build our response
            self.status = "Online"
            response = response + f"Running {util.randomPositiveEmoji()}\n\n"
        else:
            self.status = "Offline"
            response = response + f"Unknown {util.randomNegativeEmoji()}\n\n"
            return response

        # get the number of streams
        response = response + self.getCurrentPlexStreams(True)

        # get what is streaming
        response = response + self.getCurrentlyStreamingTitles()

        # get what is streaming
        response = response + f"\n{self.getFormattedServerLoad(False)}"

        # update the voice chat channel's visual status
        
        return response

    def checkStatus(self):
        return self.status

    def getFormattedServerLoad(self, formatted):
        # get the cpu usage
        cpu = util.getCPU()
        # get the ram as a percentage used
        ram = util.getRAM()
        # build the final response string
        quote = ""
        if ( formatted ):
            quote = "```"
        return f"{quote}Plex Server Load: \nCPU: {cpu}%\nRAM: {ram}%\n{quote}"

    def getActivityJson(self):
        cmd = "get_activity"
        reply = requests.get(f"http://{self.server}:{self.port}/api/v2?apikey={self.key}&cmd={cmd}").json()
        streams = self.getCurrentPlexStreamsNumber()
        if ( streams > 0 ):
            return reply
        elif( streams == 0 ):
            return 0
        else: 
            return -1

    def getCurrentlyStreamingTitles(self):
        data = self.getActivityJson()
        reply = ""
        if ( data == -1 ):
            reply = "ERROR: could not fetch currently streaming titles\n"
        elif ( data == 0 ):
            reply = ""
        else:
            sessions = data['response']['data']['sessions']
            for session in sessions:
                reply = reply + f"{session['full_title']}\n"  

        return reply

    def isPlexUpdating(self):
        if ( util.checkIfProcessRunning("Plex Update Service") ):
            return True
        return False
                    


    # makes json pretty
    # reply = json.dumps( data, indent=4, sort_keys=True)


    # def _call_api(self, cmd, payload, method='GET'):
    #     payload['cmd'] = cmd
    #     payload['apikey'] = self.connection.apikey

    #     try:
    #         response = self.connection.session.request(method, self.connection.url + '/api/v2', params=payload)
    #     except RequestException as e:
    #         print("Tautulli request failed for cmd '{}'. Invalid Tautulli URL? Error: {}".format(cmd, e))
    #         return

    #     try:
    #         response_json = response.json()
    #     except ValueError:
    #         print("Failed to parse json response for Tautulli API cmd '{}'".format(cmd))
    #         return

    #     if response_json['response']['result'] == 'success':
    #         return response_json['response']['data']
    #     else:
    #         error_msg = response_json['response']['message']
    #         print("Tautulli API cmd '{}' failed: {}".format(cmd, error_msg))
    #         return
    

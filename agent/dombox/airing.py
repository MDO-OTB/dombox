from subprocess import Popen

class Airing():
    AIRING_SCRIPT='/usr/bin/airing_AB400D_control.sh'
    airingToID={}
    airingToID['bedroom']='3'
    allowedAction = ('start','stop')
    allowedRoom = ('bedroom')

    @staticmethod
    def control(roomName,action):
        if action in Airing.allowedAction:
            command=[Airing.AIRING_SCRIPT, action,str(Airing.airingToID[roomName])]
            Popen(command)

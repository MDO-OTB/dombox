from subprocess import Popen
import time

class Shutter():
    #TODO:This script needs www-data is in gpio group
    SHUTTER_PWM_SCRIPT='/usr/bin/shutter_pwm_control.sh'
    SHUTTER_RTS_SCRIPT='/usr/bin/shutter_rts_control.sh'
    SHUTTER_STATUS_PREFIX='/tmp/shutter'
    
    roomLookupTable={}
    roomLookupTable['bedroom_camille']=('1', SHUTTER_PWM_SCRIPT)
    roomLookupTable['bedroom_remi']=('2', SHUTTER_PWM_SCRIPT)
    roomLookupTable['bedroom_parents']=('FFFFB0', SHUTTER_RTS_SCRIPT)
    roomLookupTable['kitchen']=('FFFFA0', SHUTTER_RTS_SCRIPT)
    roomLookupTable['livingRoom_east']=('FFFFD0', SHUTTER_RTS_SCRIPT)
    roomLookupTable['livingRoom_west']=('FFFFF0', SHUTTER_RTS_SCRIPT)
    roomLookupTable['bathroom']=('FFFFC0', SHUTTER_RTS_SCRIPT)

    shutterStatusToValue={}
    shutterStatusToValue['unknown']=-1
    shutterStatusToValue['closed']=0
    shutterStatusToValue['closing']=1
    shutterStatusToValue['opening']=2
    shutterStatusToValue['opened']=3
    
    allowedAction = ('open', 'stop', 'close', 'force_close', 'force_open')
    
    @staticmethod
    def get_status(motorDriver):
        try:
            with open(Shutter.SHUTTER_STATUS_PREFIX+str(motorDriver), 'r')  as f:
                statusString = f.readline()[:-1]
            status = Shutter.shutterStatusToValue[statusString]
        except:
            return -1
        return status
    
    @staticmethod
    def get_status_text(motorDriver):
        try:
            with open(Shutter.SHUTTER_STATUS_PREFIX+str(motorDriver), 'r')  as f:
                statusString = f.readline()[:-1]
        except:
            return (False,'unknown')
        return (True,statusString)
    
    @staticmethod
    def control(roomName,action):
        if action in Shutter.allowedAction:
            command=[Shutter.roomLookupTable[roomName][1], action,Shutter.roomLookupTable[roomName][0]]
            #unblocking to allow action 'stop'
            Popen(command,close_fds=False)
            #blocking
            #  shutter_process=Popen(command)
            #  retVal=shutter_process.wait()

    @staticmethod
    def control_all(action):
        room_list = list(Shutter.roomLookupTable.keys())
        for room in room_list:
            if action in Shutter.allowedAction:
                command=[shutterToScript[room], action,str(shutterToMotorDriver[room])]
                shutter_process=Popen(command)
                retVal=shutter_process.wait()
                time.sleep(2)

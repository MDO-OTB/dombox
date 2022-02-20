from subprocess import Popen

class Alarm():
    ALARM_SCRIPT='/usr/bin/alarm_AB400D_control.sh'
    ALARM_ID='1'

    @staticmethod
    def dingdong():
        command=[Alarm.ALARM_SCRIPT, "start",Alarm.ALARM_ID]
        Popen(command)

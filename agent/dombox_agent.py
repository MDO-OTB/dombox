#!/usr/bin/python3

import schedule
import time
import json
from collections import deque
import os
import logging
import logging.handlers
import pyinotify

from dombox import Airing, Alarm, Config, Sensor, Shutter

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

class Agent(pyinotify.ProcessEvent):
    PID_FILE='/var/run/dombox_agent.pid'
    SCHEDULE_QUANTUM=60
            
    def __init__(self):
        self.firstPrintDone=False
        self.logger = logging.getLogger(__name__)
        self.loopCounter = -1
        self.dayly_done = False
        touch(Sensor.RECURRENT_SAMPLES_FILEPATH)
        touch(Sensor.DAYLY_SAMPLES_FILEPATH)
        PIDFile = open(self.PID_FILE, 'w+') 
        PIDFile.write(str(os.getpid()))
        PIDFile.close()
        self.conf = Config(Config.DEFAULT_CONFIG_FILE)
        self.logger_init()
        self.measure()
        self.scheduleJobs()
        self.monitorConfig()
        self.run()

    def logger_configLevel(self):
        self.conf.acquire()
        self.logger.setLevel(self.conf.logLevel)
        self.conf.release()
        self.logger.info(self.logger_configLevel.__name__+'> level:'+str(self.conf.logLevel));
        
    def logger_init(self):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - agent - %(message)s')
        handler = logging.handlers.RotatingFileHandler(Config.DEFAULT_LOG_FILE, maxBytes=1024*1024, backupCount=1)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger_configLevel()

    def reconfig(self,signum=None, frame=None):
        self.logger.debug(self.reconfig.__name__+'>');
        oldLogLevel = self.conf.logLevel;
        self.conf.load()
        if oldLogLevel != self.conf.logLevel:
            self.logger_configLevel()
        schedule.clear()
        self.scheduleJobs()

    def process_IN_CLOSE_WRITE(self, event):
        self.reconfig()
        
    def monitorConfig(self):
        wm = pyinotify.WatchManager()
        notifier = pyinotify.ThreadedNotifier(wm,self)
        notifier.start()
        wm.add_watch(Config.DEFAULT_CONFIG_FILE, pyinotify.IN_CLOSE_WRITE)
        
    def measure(self):
        struct_time=time.localtime()
        t = int(round(time.mktime(struct_time)))
        try:
            #AM2302_1_humidity, AM2302_1_temperature = Sensor.AM2302_1_get()
            AM2302_1_humidity = 0
            AM2302_1_temperature = 0

        except:
            AM2302_1_humidity = 0
            AM2302_1_temperature = 0

#        if AM2302_1_humidity is None:
#            AM2302_1_humidity = 0
#        if AM2302_1_temperature is None:
#            AM2302_1_temperature = 0
        
        try:
            #AM2302_2_humidity, AM2302_2_temperature = Sensor.AM2302_2_get()
            AM2302_2_humidity = 0
            AM2302_2_temperature = 0

        except:
            AM2302_2_humidity = 0
            AM2302_2_temperature = 0

#        if AM2302_2_humidity is None:
#            AM2302_2_humidity = 0
#        if AM2302_2_temperature is None:
#            AM2302_2_temperature = 0

        try:
            (BMP280_pressure, BMP280_temperature) = Sensor.bmp280_get()
        except:
            BMP280_temperature = 0
            BMP280_pressure = 0

        #try:
        #    BMP085_temperature = self.BMP085_sensor.read_temperature()
        #except:
        #    BMP085_temperature = 0
        #try:
        #    BMP085_pressure = self.BMP085_sensor.read_pressure()
        #except:
        #    BMP085_pressure = 0
            
        shutter1 = Shutter.get_status(1)
        shutter2 = Shutter.get_status(2)
        
        samples =(t, (round(AM2302_1_humidity,2),round(AM2302_1_temperature,2)), (round(AM2302_2_humidity,2),round(AM2302_2_temperature,2)),(round(BMP280_temperature,2), int(BMP280_pressure)),(shutter1,shutter2) )
        samples_json = json.dumps(samples)
        if self.firstPrintDone is False:
            print(str(samples))
            self.firstPrintDone = True
        
        with open(Sensor.RECURRENT_SAMPLES_FILEPATH) as f:
            buffer = deque(f, maxlen=self.conf.SAMPLES_MAX)
        buffer.append(samples_json + '\n')
        with open(Sensor.RECURRENT_SAMPLES_FILEPATH, 'w') as f:
            f.writelines(buffer)
        self.logger.debug(self.measure.__name__+'> recurrent done');
        if (struct_time.tm_hour % self.conf.DAYLY_SAMPLES_HOURS) == 0 and self.dayly_done == False: 
            with open(Sensor.DAYLY_SAMPLES_FILEPATH) as f:
                buffer = deque(f, maxlen=self.conf.DAYLY_SAMPLES_MAX)
            buffer.append(samples_json + '\n')
            with open(Sensor.DAYLY_SAMPLES_FILEPATH, 'w') as f:
                f.writelines(buffer)
            self.dayly_done=True
            self.logger.debug(self.measure.__name__+'> daily done');
        elif (struct_time.tm_hour % self.conf.DAYLY_SAMPLES_HOURS) != 0:
            self.dayly_done=False
        
        self.conf.acquire()
        if self.conf.tempControlShutter:
            if AM2302_2_temperature > self.conf.tempMaxThresholdOpen:
                self.logger.info(self.measure.__name__+'> '+str(AM2302_2_temperature)+'C >'+str(self.conf.tempMaxThresholdOpen)+'C open shutters');
                self.openRoofShutter()
            if AM2302_2_temperature < self.conf.tempMinThresholdOpen:
                self.logger.info(self.measure.__name__+'> '+str(AM2302_2_temperature)+'C <'+str(self.conf.tempMinThresholdOpen)+'C open shutters');
                self.openRoofShutter()
            if AM2302_2_temperature > self.conf.tempMaxThresholdClose:
                self.logger.info(self.measure.__name__+'> '+str(AM2302_2_temperature)+'C >'+str(self.conf.tempMaxThresholdClose)+'C close shutters');
                self.closeRoofShutter()
            if AM2302_2_temperature < self.conf.tempMinThresholdClose:
                self.logger.info(self.measure.__name__+'> '+str(AM2302_2_temperature)+'C <'+str(self.conf.tempMinThresholdClose)+'C close shutters');
                self.closeRoofShutter()
        self.conf.release()

    def actionAiring(self,room, action):
        self.logger.info('airing>'+action+'>'+room);
        Airing.control(room, action)

    def actionShutter(self,room,action):
        self.logger.info('shutter>'+action+'>'+room);
        Shutter.control(room, action)

    def scheduleJobs(self):
        self.conf.acquire()
        if self.conf.measureEnabled:
            schedule.every(self.conf.SAMPLES_DELAY).seconds.do(self.measure)
        
        if self.conf.timeControlAiring:
            schedule.every().day.at(self.conf.airingRoomStartHour).do(self.actionAiring, room='bedroom', action='start')
            schedule.every().day.at(self.conf.airingRoomStopHour).do(self.actionAiring, room='bedroom', action='stop')
        
        if self.conf.alarmEnabled:
            schedule.every().day.at(self.conf.alarmHour).do(Alarm.dingdong)
        
        if self.conf.timeControlShutter:
            schedule.every().day.at(self.conf.roofOpenHour).do(self.actionShutter, room='bedroom_camille', action='open')
            schedule.every().day.at(self.conf.roofOpenHour).do(self.actionShutter, room='bedroom_remi', action='open')
            
            schedule.every().day.at(self.conf.roofCloseHour).do(self.actionShutter, room='bedroom_camille', action='close')
            schedule.every().day.at(self.conf.roofCloseHour).do(self.actionShutter, room='bedroom_remi', action='close')

            schedule.every().day.at(self.conf.kitchenOpenHour).do(self.actionShutter, room='kitchen', action='open')
            schedule.every().day.at(self.conf.kitchenCloseHour).do(self.actionShutter, room='kitchen', action='close')
            
            schedule.every().day.at(self.conf.bathroomOpenHour).do(self.actionShutter, room='bathroom', action='open')
            schedule.every().day.at(self.conf.bathroomCloseHour).do(self.actionShutter, room='bathroom', action='close')

            schedule.every().day.at(self.conf.bedroomOpenHour).do(self.actionShutter, room='bedroom_parents', action='open')
            schedule.every().day.at(self.conf.bedroomCloseHour).do(self.actionShutter, room='bedroom_parents', action='close')
            
            schedule.every().day.at(self.conf.livingRoomEastOpenHour).do(self.actionShutter, room='livingRoom_east', action='open')
            schedule.every().day.at(self.conf.livingRoomEastCloseHour).do(self.actionShutter, room='livingRoom_east', action='close')
   
            schedule.every().day.at(self.conf.livingRoomWestOpenHour).do(self.actionShutter, room='livingRoom_west', action='open')
            schedule.every().day.at(self.conf.livingRoomWestCloseHour).do(self.actionShutter, room='livingRoom_west', action='close')

        self.conf.release()

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(Agent.SCHEDULE_QUANTUM)
    
if __name__ == '__main__':
    C = Agent()

    

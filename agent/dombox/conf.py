
import json
import logging
import threading


class Config():
    DEFAULT_CONFIG_FILE='/etc/domConfig'
    DEFAULT_LOG_FILE='/tmp/log_roof'
    def __init__(self,pathname):
        self.mutex = threading.Lock()
        self.pathname = pathname
        self.load()

    def __str__(self):
        self.acquire()
        out = 'measureEnabled: ' + str(self.measureEnabled) + '\n'
        out += 'SAMPLES_DELAY: ' + str(self.SAMPLES_DELAY)  + '\n'
        out += 'SAMPLES_MAX: ' + str(self.SAMPLES_MAX)  + '\n'
        out += 'DAYLY_SAMPLES_HOURS: ' + str(self.DAYLY_SAMPLES_HOURS)  + '\n'
        out += 'DAYLY_SAMPLES_MAX: ' + str(self.DAYLY_SAMPLES_MAX)  + '\n'
        out += 'timeControlShutter: ' + str(self.timeControlShutter)  + '\n'
        out += 'timeControlAiring: ' + str(self.timeControlAiring)  + '\n'
        out += 'tempControlShutter: ' + str(self.tempControlShutter)  + '\n'
        if self.timeControlShutter is True:
            out += 'roofOpenHour: ' + self.roofOpenHour  + '\n'
            out += 'roofCloseHour: ' + self.roofCloseHour  + '\n'
            out += 'kitchenOpenHour: ' + self.kitchenOpenHour  + '\n'
            out += 'kitchenCloseHour: ' + self.kitchenCloseHour  + '\n'
            out += 'bathroomOpenHour: ' + self.bathroomOpenHour  + '\n'
            out += 'bathroomCloseHour: ' + self.bathroomCloseHour  + '\n'
            out += 'bedroomOpenHour: ' + self.bedroomOpenHour  + '\n'
            out += 'bedroomCloseHour: ' + self.bedroomCloseHour  + '\n'
            out += 'livingRoomEastOpenHour: ' + self.livingRoomEastOpenHour  + '\n'
            out += 'livingRoomEastCloseHour: ' + self.livingRoomEastCloseHour  + '\n'
            out += 'livingRoomWestOpenHour: ' + self.livingRoomWestOpenHour  + '\n'
            out += 'livingRoomWestCloseHour: ' + self.livingRoomWestCloseHour  + '\n'
        if self.timeControlAiring is True:
            out += 'airingRoomStartHour: ' + self.airingRoomStartHour  + '\n'
            out += 'airingRoomStopHour: ' + self.airingRoomStopHour  + '\n'
        out += 'alarmEnabled: ' + str(self.alarmEnabled)  + '\n'
        if self.alarmEnabled is True:
            out += 'alarmHour: ' + self.alarmHour  + '\n'
        if self.tempControlShutter is True:
            out += 'tempMaxThresholdOpen' + str(self.tempMaxThresholdOpen) + '\n'
            out += 'tempMinThresholdOpen' + str(self.tempMinThresholdOpen) + '\n'
            out += 'tempMaxThresholdClose' + str(self.tempMaxThresholdClose) + '\n'
            out += 'tempMinThresholdClose' + str(self.tempMinThresholdClose) + '\n'
        out += 'self.logLevel: ' + str(self.logLevel) + '\n'
        self.release()
        return out

    @staticmethod
    def parseLogLevel(string):
        try:
            if string == "CRITICAL":
                logLevel  = logging.CRITICAL
            elif string == "ERROR":
                logLevel  = logging.ERROR
            elif string == "WARNING":
                logLevel  = logging.WARNING
            elif string == "INFO":
                logLevel  = logging.INFO
            elif string == "DEBUG":
                logLevel  = logging.DEBUG
            else:
                logLevel  = logging.DEBUG
        except:
            logLevel=logging.DEBUG
        return logLevel

    @staticmethod
    def load_json(pathname):
        configFile = open(pathname, 'r')
        line = configFile.readline()
        config = json.loads(line)
        configFile.close()
        return config
    
    @staticmethod
    def load_logLevel(pathname):
        try:
            config = Config.load_json(pathname)
            return Config.parseLogLevel(config["logLevel"])
        except:
            return logging.DEBUG
        
    def load(self):
        config = Config.load_json(self.pathname)
        self.acquire()
        self.SAMPLES_DELAY=config["delayMeasure"]
        self.SAMPLES_MAX=config["maxSamples"]
        self.DAYLY_SAMPLES_HOURS=int(round(24/config["maxDailySamplesADay"]))
        self.DAYLY_SAMPLES_MAX=config["maxDailySamples"]
        self.measureEnabled = config["measureEnabled"]
        
        self.tempControlShutter = config["tempControlShutter"]
        if self.tempControlShutter:
            try:
                self.tempMaxThresholdOpen=config["tempMaxThresholdOpen"]
                self.tempMinThresholdOpen=config["tempMinThresholdOpen"]
                self.tempMaxThresholdClose=config["tempMaxThresholdClose"]
                self.tempMinThresholdClose=config["tempMinThresholdClose"]
            except:
                print("Failed to configure temperatur for opening or closing shutter")
                self.tempControlShutter = False
            
        self.timeControlShutter = config["timeControlShutter"]
        if self.timeControlShutter:
            try:
                self.roofOpenHour = "%02d:%02d" % (config["roofOpenHour"], config["roofOpenMinute"])
                self.roofCloseHour = "%02d:%02d" % (config["roofCloseHour"], config["roofCloseMinute"])
                self.kitchenOpenHour = "%02d:%02d" % (config["kitchenOpenHour"], config["kitchenOpenMinute"])
                self.kitchenCloseHour = "%02d:%02d" % (config["kitchenCloseHour"], config["kitchenCloseMinute"])
                self.bathroomOpenHour = "%02d:%02d" % (config["bathroomOpenHour"], config["bathroomOpenMinute"])
                self.bathroomCloseHour = "%02d:%02d" % (config["bathroomCloseHour"], config["bathroomCloseMinute"])
                self.bedroomOpenHour = "%02d:%02d" % (config["bedroomOpenHour"], config["bedroomOpenMinute"])
                self.bedroomCloseHour = "%02d:%02d" % (config["bedroomCloseHour"], config["bedroomCloseMinute"])
                self.livingRoomEastOpenHour = "%02d:%02d" % (config["livingRoomEastOpenHour"], config["livingRoomEastOpenMinute"])
                self.livingRoomEastCloseHour = "%02d:%02d" % (config["livingRoomEastCloseHour"], config["livingRoomEastCloseMinute"])
                self.livingRoomWestOpenHour = "%02d:%02d" % (config["livingRoomWestOpenHour"], config["livingRoomWestOpenMinute"])
                self.livingRoomWestCloseHour = "%02d:%02d" % (config["livingRoomWestCloseHour"], config["livingRoomWestCloseMinute"])
            except:
                print("Failed to configure opening or closing timetable fot shutter.")
                self.timeControlShutter = False
                            
        self.timeControlAiring = config["timeControlAiring"]
        if self.timeControlAiring:
            try:
                self.airingRoomStartHour = "%02d:%02d" % (config["airingRoomStartHour"], config["airingRoomStartHour"])
                self.airingRoomStopHour = "%02d:%02d" % (config["airingRoomStopHour"], config["airingRoomStopMinute"])
            except:
                print("Failed to configure opening or closing timetable for airing.")
                self.timeControlAiring = False

        self.alarmEnabled = config["alarm"]
        if self.alarmEnabled:
            try:
                self.alarmHour = "%02d:%02d" % (config["alarmHour"], config["alarmMinute"])
            except:
                print("Failed to configure opening or closing timetable for alarm.S")
                self.alarmEnabled = False
        
        self.logLevel = Config.parseLogLevel(config["logLevel"])
        self.release()
        print(self)

    def acquire(self):
        self.mutex.acquire()

    def release(self):
        self.mutex.release()

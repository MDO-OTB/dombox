#!/usr/bin/python3
from flup.server.fcgi import WSGIServer
import urllib.parse
import logging
import logging.handlers
from socket import gethostname
import netifaces as ni
import json

from dombox import Airing, Alarm, Config, Sensor, Shutter

allowedWhat = ('top','log','temperature', 'humidity', 'pressure', 'conf', 'shutter')
BACKEND_VERSION='0.2'
logger = logging.getLogger(__name__)

def logger_configLevel():
    try:
      loggerLevel = Config.load_logLevel(Config.DEFAULT_CONFIG_FILE)
    except:
      loggerLevel  = logging.DEBUG
    logger.setLevel(loggerLevel)
    logger.info(logger_configLevel.__name__+'> level:'+str(loggerLevel));
    
def logger_init():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - webserver -%(message)s')
    handler = logging.handlers.RotatingFileHandler(Config.DEFAULT_LOG_FILE, maxBytes=1024*1024, backupCount=1)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger_configLevel()

def goodRequest(start_response):
    start_response('200 OK', [('Content-Type', 'text/json'),('Access-Control-Allow-Origin','*')])
    #('Access-Control-Allow-Origin','*')

def emptyResponse(start_response):
    start_response("204 No Content", [("Content-Type", "text/html")]) 

def badRequest(error, start_response):
    start_response(error, [("Content-Type", "text/html")])

def getTopInfo():
    host_name=''
    host_ip=''
    host_uptime=''
    try:
        host_name=gethostname()
        host_ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        with open('/proc/uptime', 'r') as f:
            host_uptime = float(f.readline().split()[0])
        return (True,BACKEND_VERSION, host_name, host_ip, host_uptime)
    except:
        return (False,BACKEND_VERSION, host_name, host_ip, host_uptime)

def getLog():
    try:
        with open(Config.DEFAULT_LOG_FILE, 'r') as f:
            log = f.readlines()
        logger.debug(getLog.__name__+'>'+'success');
        return (True,log[-100:])
    except:
        logger.error(getLog.__name__+'>'+'failed');
        return (False,'failed')

def processGETConf():
    try:
        configFile = open(Config.DEFAULT_CONFIG_FILE, 'r') 
        conf=configFile.read()
        configFile.close()
    except:
        logger.error(processGETConf.__name__+'>'+str((False,'error')));
        return (False,'error')
    logger.debug(processGETConf.__name__+'>'+str((True,conf)));
    return (True,conf)

def processPOSTConf(environ):
    try:
        post_data_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        logger.debug(processPOSTConf.__name__+'>'+'ValueError');
        return False
    
    confBytes = environ['wsgi.input'].read(post_data_size)
    conf = confBytes.decode('utf-8')
    logger.debug(processPOSTConf.__name__+'>'+conf);
    try:
        configFile = open(Config.DEFAULT_CONFIG_FILE, 'w+') 
        configFile.write(conf)
        configFile.close()
    except:
        logger.error(processPOSTConf.__name__+'>'+'Error');
        return False
    logger_configLevel()
    return True

def clearLog():
    logger.debug(clearLog.__name__+'>'+'init');
    try:
        with open(Config.DEFAULT_LOG_FILE, 'w'):
            pass
    except:
        logger.error(clearLog.__name__+'>'+'Error');
        return False
    logger.debug(clearLog.__name__+'>'+'Success');
    return True

def serve(environ, start_response):
    try:
        typeRequest = environ.get('REQUEST_METHOD')
    except ValueError:
        typeRequest =''
    # and typeRequest != 'POST':
    if typeRequest != 'GET' and typeRequest != 'POST': 
        badRequest('501 Unavailable',start_response)
        return ('&nbsp;')
    param = urllib.parse.parse_qs(environ["QUERY_STRING"])
    logger.debug(serve.__name__+'>'+typeRequest+ ';'+str(param));

    if 'what' in param :
        what = param['what'][0]
    else:
        what = None

    if 'step' in param :
        step = param['step'][0]
    else:
        step = None

    if 'shutter' in param :
        shutter = param['shutter'][0]
    else:
        shutter = None
    if 'airing' in param :
        airing = param['airing'][0]
    else:
        airing = None

    if 'action'  in param:
        action = param['action'][0]
    else:
        action = None

    if (what is None and shutter is None and airing is None):
        badRequest("400 Bad Request",start_response)
        return ('&nbsp;')

    if shutter:
        if typeRequest == 'POST' and action in Shutter.allowedAction and shutter in list(Shutter.roomLookupTable.keys()):
            goodRequest(start_response)
            if shutter == 'house':
              Shutter.control_all(action)
            else:
              Shutter.control(shutter,action)
            return ('&nbsp;')
        elif typeRequest == 'GET' and shutter in list(Shutter.roomLookupTable.keys()):
            (result,status) = Shutter.get_status_text(Shutter.roomLookupTable[shutter][0])
            if result == True:
                goodRequest(start_response)
                return status
        badRequest('512 Unavailable',start_response)
        return ('&nbsp;')
    elif airing:
        if typeRequest == 'POST' and action in Airing.allowedAction and airing in Airing.allowedRoom:
            goodRequest(start_response)
            Airing.control(airing,action)
            return ('&nbsp;')
        badRequest('512 Unavailable',start_response)
        return ('&nbsp;')
    elif what:
        if typeRequest == 'POST':
            result=False
            if what =='conf':
                result = processPOSTConf(environ)
            elif what =='log':
                result = clearLog()
            if result == True:
                goodRequest(start_response)
            else:
                badRequest('505 Unavailable',start_response)
            return ('&nbsp;')
        elif what not in allowedWhat:
            badRequest('507 Unavailable',start_response)
            return ('&nbsp;')
        #        if typeRequest == 'GET': ?
        elif what == 'top':
            (result,BACKEND_VERSION, host_name, host_ip, host_uptime) = getTopInfo()
            if result is False:
                badRequest('502 Unavailable',start_response)
                return ('&nbsp;')
            else:
                goodRequest(start_response)
                return json.dumps((BACKEND_VERSION, host_name, host_ip, host_uptime))
        elif what == 'log':
            (result,log) = getLog()
            if result is False:
                badRequest('502 Unavailable',start_response)
                return ('&nbsp;')
            else:
                goodRequest(start_response)
#                return ("\n".join(log))
                return (log)
        elif what == 'conf':
            (result,conf) = processGETConf()
            if result is False:
                badRequest('503 Unavailable',start_response)
                return ('&nbsp;')
            goodRequest(start_response)
            return (conf)

        if step is None:
            badRequest('511 Unavailable',start_response)
            return ('&nbsp;')
        logger.debug('samples_get>'+str(what)+';'+str(step));    
        (dataResult,timestamp,temperature1,temperature2,temperature3,humidity1,humidity2, pressure, shutter1,shutter2) = Sensor.samples_get(what,step)
        if dataResult is False:
            badRequest('508 Unavailable',start_response)
            return ('&nbsp;')
        goodRequest(start_response)
        if what  == 'temperature':
            logger.debug(serve.__name__+'>'+str((timestamp,temperature1,temperature2,temperature3)));
            return json.dumps((timestamp,temperature1,temperature2,temperature3))
        elif what  == 'humidity':
            logger.debug(serve.__name__+'>'+str((timestamp,humidity1,humidity2)));
            return json.dumps((timestamp,humidity1,humidity2))
        elif what  == 'pressure':
            logger.debug(serve.__name__+'>'+str((timestamp,pressure)));
            return json.dumps((timestamp,pressure))
        elif what  == 'shutter':
            logger.debug(serve.__name__+'>'+str((timestamp,shutter1, shutter2)));
            return json.dumps((timestamp,shutter1, shutter2))
            
if __name__ == '__main__':
    logger_init()
    WSGIServer(serve).run()

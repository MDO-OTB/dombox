from subprocess import Popen, PIPE
import json
import Adafruit_DHT
#import Adafruit_BMP.BMP085 as BMP085

class Sensor():
    RECURRENT_SAMPLES_FILEPATH='/tmp/recurrent_samples'
    DAYLY_SAMPLES_FILEPATH='/tmp/daily_samples'
    AM2302_1_PIN='P9_12'
    AM2302_2_PIN='P9_23'
    BMP085_BUS=2
    BMP085_command=["/root/bmp280/bmp280"]
    AM2302_sensor = Adafruit_DHT.AM2302
    #BMP085_sensor = BMP085.BMP085(busnum=Sensor.BMP085_BUS, mode=BMP085.BMP085_ULTRAHIGHRES)

    @staticmethod
    def bmp280_get():
    #unblocking to allow action 'stop'
        bmp280_process=Popen(Sensor.BMP085_command, stdout=PIPE, stderr=PIPE,universal_newlines=True)
        stdout, stderr = bmp280_process.communicate()
        samples=json.loads(stdout);
        return (samples["Pressure"],samples["Temperature"])

    @staticmethod
    def AM2302_1_get():
        Adafruit_DHT.read_retry(Sensor.AM2302_sensor, Sensor.AM2302_1_PIN)

    @staticmethod
    def AM2302_2_get():
        Adafruit_DHT.read_retry(Sensor.AM2302_sensor, Sensor.AM2302_2_PIN)

    @staticmethod
    def samples_get(what,step):
        timestamp = []
        temperature1 = []
        temperature2 = []
        temperature3 = []
        humidity1 = []
        humidity2 = []
        pressure = []
        shutter1 = []
        shutter2 = []
        try:
            if step == 'hour':
                samplesFile = open(Sensor.RECURRENT_SAMPLES_FILEPATH, 'r')
            elif step == 'day':
                samplesFile = open(Sensor.DAYLY_SAMPLES_FILEPATH, 'r')
            else:
                return (False, timestamp,temperature1,temperature2,temperature3,humidity1,humidity2, pressure, shutter1,shutter2)
            for line in samplesFile.readlines():
                samples = json.loads(line)
                timestamp.append(samples[0])
                if what  == 'temperature':
                    temperature1.append(samples[1][1])
                    temperature2.append(samples[2][1])
                    temperature3.append(samples[3][0])
                elif what  == 'humidity':
                    humidity1.append(samples[1][0])
                    humidity2.append(samples[2][0])
                elif what  == 'pressure':
                    pressure.append(samples[3][1])
                elif what  == 'shutter':
                    shutter1.append(samples[4][0])
                    shutter2.append(samples[4][1])
        except:
            samplesFile.close()
            return (False, timestamp,temperature1,temperature2,temperature3,humidity1,humidity2, pressure, shutter1,shutter2)

        samplesFile.close()
        return (True, timestamp,temperature1,temperature2,temperature3,humidity1,humidity2, pressure, shutter1,shutter2)

import urllib2
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_DHT


# constants
delay = 10
APIkey = "G83WSXL23ZUC4WAD" # use your own APIkey
lightPin = 15
DHTPin = 14


GPIO.setmode(GPIO.BCM)
GPIO.setup(lightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def getHumidityTemp():

    humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHTPin)

    # Celsius to Farenheit
    tempF = 9/5*temp+32

    return (str(humidity), str(temp),str(tempF))


def getLight(lightPin):

    light = 0
    
    if (GPIO.input(lightPin) == True):
        light += 1

    return (str(light))
    

def main():
    
    print 'starting...'

    rootURL = 'https://api.thingspeak.com/update?api_key=%s' % APIkey

    while True:
        try:
            humidity, temp, tempF = getHumidityTemp()
            light = getLight(lightPin)
            con = urllib2.urlopen(rootURL + 
                                "&field1=%s&field2=%s&field3=%s" % (temp, tempF, humidity)+
                                "&field4=%s" % (light))
            print "temperature C: " + temp + " temperature F: " + tempF + " rel. humidity: " + humidity + " light: " + light
            con.close()
            sleep(int(delay))
        except:
            print 'exiting'
            break

while 1:
	main()

exit (0)

__author__ = 'rpakalap'

import RPi.GPIO as GPIO
import time
import urllib2
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
PiOut = 27
print "Distance Measurement In Progress"
b=int(round(time.time()))
while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.setup(PiOut,GPIO.OUT)
    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print "Distance:",distance,"cm"
    if distance > 2 and distance < 400:
      #Check whether the distance is within range
        if distance < 5 :
            GPIO.output(PiOut, GPIO.HIGH)
            status="NEW"
        else:
            GPIO.output(PiOut, GPIO.LOW)
            print "Distance:",distance - 0.5,"cm" #Print distance with 0.5 cm calibration
            status="RESOLVED"

        try:
            response = urllib2.urlopen("https://www.rollbase.com/rest/api/login?loginName=ram1023&password=Progress@123").read()
            start = "<sessionId>"
            end = "</sessionId>"
            token=(response.split(start))[1].split(end)[0]
            waterLevel="https://www.rollbase.com/rest/api/update2?sessionId="+token+"&objName=Garbage&id=165074138&StatusField="+status
            print waterLevel
            urllib2.urlopen(waterLevel).read()
        except:
            print "Exception"

        GPIO.cleanup()

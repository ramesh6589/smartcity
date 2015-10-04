

import RPi.GPIO as GPIO, time, os
import urllib2
DEBUG = 1
GPIO.setmode(GPIO.BCM)
PiOut=18
GPIO.setup(PiOut, GPIO.OUT)
def RCtime (RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading
try:
  while True:
          reading = RCtime(13)# Read RC timing using pin #18
          print reading
          if reading < 300 :
            GPIO.output(PiOut, GPIO.HIGH)
            status="NEW"
          else:
            GPIO.output(PiOut, GPIO.LOW)
            status="RESOLVED"

          try:
            response = urllib2.urlopen("https://www.rollbase.com/rest/api/login?loginName=ram1023&password=Progress@123").read()
            start = "<sessionId>"
            end = "</sessionId>"
            token=(response.split(start))[1].split(end)[0]
            waterLevel="https://www.rollbase.com/rest/api/update2?sessionId="+token+"&objName=landscapes&id=165074123&landscapeStatus="+status
            print waterLevel
            urllib2.urlopen(waterLevel).read()

          except:
            print "Exception"
except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()
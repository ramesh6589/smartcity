

import RPi.GPIO as GPIO, time, os

DEBUG = 1
GPIO.setmode(GPIO.BCM)
PiOut=5
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
          reading = RCtime(12)# Read RC timing using pin #18
          if reading > 1000 :
            GPIO.output(PiOut, GPIO.HIGH)
          else:
            GPIO.output(PiOut, GPIO.LOW)
except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()
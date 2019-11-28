#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

class sensor:
    def __init__(self):
        self.TRIG = 11
        self.ECHO = 13

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, GPIO.LOW)

        time.sleep(0.1)

        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

    def exe(self):
        while GPIO.input(self.ECHO) == 0:
            signaloff = time.time()

        while GPIO.input(self.ECHO) == 1:
            signalon = time.time()

        timepassed = signalon - signaloff
        print("time span:{}".format(timepassed))
        GPIO.cleanup()
        return timepassed * 17000


"""
def reading(sensor):
    import time
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
     
    GPIO.setmode(GPIO.BOARD)
    TRIG = 11
    ECHO = 13
     
    if sensor == 0:
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, GPIO.LOW)
        time.sleep(0.3)
         
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
 
        while GPIO.input(ECHO) == 0:
          signaloff = time.time()
         
        while GPIO.input(ECHO) == 1:
          signalon = time.time()
 
        timepassed = signalon - signaloff
        print("timepassed = " + str(timepassed))
        distance = timepassed * 17000
        return distance
        GPIO.cleanup()

    else:
        print("Incorrect usonic() function varible.")
"""


def main():
    s = sensor()
    while True:
        s.setup()
        print(s.exe())

if __name__ == '__main__':
    main()
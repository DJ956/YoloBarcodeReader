#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

RANGE = 3

class sensor:
    def __init__(self):
        #self.TRIG = 11
        self.TRIG = 17
        #self.ECHO = 13
        self.ECHO = 27
        self.sum = 0
        self.avg = 0
        self.dis = 0

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, GPIO.LOW)

        time.sleep(0.15)

        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        #GPIO.cleanup()

    def exe(self):
        while GPIO.input(self.ECHO) == 0:
            signaloff = time.time()

        while GPIO.input(self.ECHO) == 1:
            signalon = time.time()

        timepassed = signalon - signaloff
        #print("time span:{}".format(timepassed))
        #GPIO.cleanup()
        return timepassed * 17000

    def get_flag(self):
        flag = -1
        cnt = 0
        self.sum = 0
        while cnt < 15:
            self.setup()
            self.dis = self.exe()
            self.sum = self.sum + self.dis
            cnt = cnt + 1

        self.avg = float(self.sum / 15)
        if self.dis < float(self.avg - RANGE):
            flag = 1
        else:
            flag = 0

        return flag

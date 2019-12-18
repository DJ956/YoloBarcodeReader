#! /usr/bin/python3

import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

RANGE = 3
class sensor_w:

    def __init__(self):
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(-57)
        self.hx.reset()
        self.hx.tare()

        self.inc_flag = 0
        self.g_weight = 0
        self.val = -1
        print("Tare done! Add weight now...")     

    def exe(self):   
        self.inc_flag = 0
        try:
            self.val = self.hx.get_weight(5)

            if float(-self.val) < float(self.g_weight - RANGE):
                self.inc_flag = -1
                self.g_weight = -self.val
            elif float(self.g_weight + RANGE) < float(-self.val):
                self.inc_flag = 1
                self.g_weight = -self.val

            self.hx.power_down()
            self.hx.power_up()
            time.sleep(0.1)

            return self.inc_flag
        except(KeyboardInterrupt, SystemExit):
            self.cleanAndExit()


    def cleanAndExit(self):
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
        sys.exit()

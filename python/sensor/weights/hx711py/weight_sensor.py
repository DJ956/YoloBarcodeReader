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

        self.inc_flag = False
        self.g_weight = 0
        self.val = -1

    def exe(self):
        print("Tare done! Add weight now...")        
        self.inc_flag = False
        try:
            self.val = self.hx.get_weight(5)

            if float(-self.val) < float(RANGE):
                self.g_weight = -val
            elif float(self.g_weight + RANGE) < float(-self.val):
                self.inc_flag = True
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

"""
while True:
    try:
        val = hx.get_weight(5)
        print("{}g".format(-val))


#        if g_weight < float(RANGE):
#            inc_flag = -1
#            print("Flag:{} g_weight:{}".format(inc_flag, g_weight))

        if float(-val) < float(RANGE):
            print("Flag:{} g_weight:{}".format(inc_flag, g_weight))
            g_weight = -val

        elif float(g_weight + RANGE) < float(-val):
            inc_flag = True
            print("Flag:{} g_weight:{}".format(inc_flag, g_weight))

            time.sleep(3) #信号受けとってから
            
            g_weight = -val
            inc_flag = -1

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
"""
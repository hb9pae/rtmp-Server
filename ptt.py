#!/usr/bin/python
# -*- coding: latin-1 -*-
# PTT Signal

import RPi.GPIO as GPIO
#from time import sleep
import time

PORT = 40

GPIO.cleanup()

GPIO.setmode (GPIO.BOARD)

#GPIO.setmode (GPIO.BCM)
GPIO.setup (PORT,GPIO.OUT)


while True:
    GPIO.output(PORT,True)
    time.sleep(5)
    GPIO.output(PORT,False)
    time.sleep(5) 


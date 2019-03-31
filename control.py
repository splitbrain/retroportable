#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import subprocess
import sys

# pins for the LEDs
pin_g = 22
pin_y = 27
pin_r = 17
# pin for the fan
pin_fan = 14
# pin for the volume button
pin_vol = 6

# temperature thresholds in Celsius
low = 55
mid = 65
high = 75

# volumes to cycle through and current index
volumes = [100, 80, 45, 0]
volume = 0

# callback for the volume button
def cycle_volume(channel):
    global volume
    volume += 1
    if volume >= len(volumes):
        volume = 0
    print("volume %d" % volumes[volume])
    subprocess.call(['/usr/bin/amixer','sset', 'PCM', str(volumes[volume])+'%'])
    subprocess.call(['/usr/bin/aplay', sys.path[0] + '/beep.wav'])

# initialize with full volume
subprocess.call(['/usr/bin/amixer','sset', 'PCM', str(volumes[volume])+'%'])

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_g, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_y, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_r, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_fan, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_vol, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pin_vol, GPIO.FALLING, callback=cycle_volume, bouncetime=300)

# read temperatures every ten seconds
try:
    tfile = open('/sys/class/thermal/thermal_zone0/temp')
    while True:
        tfile.seek(0)
        temp = float(tfile.read()) / 1000
        print temp
 
        GPIO.output(pin_g, temp > low)
        GPIO.output(pin_y, temp > mid)
        GPIO.output(pin_r, temp > high)
        GPIO.output(pin_fan, temp > mid)
 
        sleep(10);
except:
    print "exiting"
finally:
    tfile.close()
    GPIO.cleanup()

# -*- coding: cp1257 -*-

import Adafruit_DHT as tempsensor
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import mh_z19

import time
from datetime import datetime as clock
from datetime import timedelta

import os
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import init


DHT_SENSOR = tempsensor.DHT22
DHT_PIN  = 4
SAMPLE_TIME = 60



try:
    os.remove('testlog.csv')
    os.remove('max.csv')

except:
    pass

try:
 
    file = open('/home/pi/Study_Fresh/Beta/testlog.csv', 'a+')
    log = open('/home/pi/Study_Fresh/Beta/max.csv','a+')
    
    if os.stat('/home/pi/Study_Fresh/Beta/testlog.csv').st_size == 0:
        
        file.write('Timestamp (MM/DD/YYYY HH:MM),Temperature (�C),Humidity (%),Co2 (ppm)\r\n')
        log.write('Delta (sec)\r\n')
except:
    pass

RST = 24
# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst = RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bitt color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline = 0, fill = 0)


# First define some constants to allow easy resizing of shapes.
padding = 1
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.truetype('Mario-Kart-DS.ttf',36)

draw.text((x, top + 1), "study",  font=font, fill=255)
draw.text((x, top + 33), "    fresh",  font=font, fill=255)

disp.image(image)
disp.display()
time.sleep(1)

draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

font = ImageFont.truetype('Mario-Kart-DS.ttf',40)
draw.text((x, top + 1), "BY UQ",  font=font, fill=255)

font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',16)
draw.text((x, top + 47), "    loading...",  font=font, fill=255)

# Display image.
disp.image(image)
disp.display()

font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',15)

try:
    
    # Get Sensor Data
    humidity, temperature = tempsensor.read(DHT_SENSOR, DHT_PIN)
    Co2 = mh_z19.read_all()['co2']    
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    # Write text.
    if humidity is not None and temperature is not None: 
        
        draw.text((x, top + 0),  "Co2 : " + str(Co2).rjust(4,' ') + " PPM",  \
                  font=font, fill=255)
        draw.text((x, top + 16), "TEM : " + "{:.1f}".format(temperature) + " C",  \
                  font=font, fill=255)
        draw.text((x, top + 32), "HUM : " + "{:.1f}".format(humidity) + " %",  \
                  font=font, fill=255)
        
        startTime = clock.now()
        
        draw.text((x, top + 48),  startTime.strftime('%d/%m %H:%M:%S'),  \
                  font=font, fill=255)
        
        file.write('{0},{1:0.1f},{2:0.1f}%,{3}\r\n'.format(startTime.strftime('%x %X'),\
                                                           temperature, humidity, Co2))
                    
        print('{0},{1:0.1f},{2:0.1f}%,{3}\r\n'.format(startTime.strftime('%x %X'),\
                                                      temperature, humidity, Co2))
        
    else:
        
        draw.text((x, top + 0),  "Co2 : " + "ERROR",  font=font, fill=255)
        draw.text((x, top + 16), "TEM : " + "ERROR",  font=font, fill=255)
        draw.text((x, top + 32), "HUM : " + "ERROR",  font=font, fill=255)
            
        startTime = clock.now()
        draw.text((x, top + 48),  startTime.strftime('%d/%m %H:%M:%S'),  \
                  font=font, fill=255)     

    # Display image.
    disp.image(image)
    disp.display()
    
    Diff = 0
    Diff2 = 0
    
    while True:
        
        try:
            
            
            # Get Sensor Data
            humidity, temperature = tempsensor.read_retry(DHT_SENSOR, DHT_PIN)
            time.sleep(2)
            
            Co2 = mh_z19.read_all()['co2']
            time.sleep(2)
            
            if Diff > 1:
                Diff2 = Diff
            
            Diff = (clock.now()-startTime).total_seconds()
            Delta = Diff - Diff2
            
            print("Diff = {0:.6f} Delta = {1:.6f}\r".format(Diff, Delta))
            # print("Diff = {0:.6f}\r".format(Diff))
            
            if Delta > 10:
                 log.write('{0},{1:.6f}\r\n'.format(startTime.strftime('%x %X'),Delta))
            
            if Diff > (0.5 * SAMPLE_TIME):

                # Draw a black filled box to clear the image.
                draw.rectangle((0,0,width,height), outline=0, fill=0)
    
                # Write text.
                if humidity is not None and temperature is not None: 
        
                    draw.text((x, top + 0),  "Co2 : " + str(Co2).rjust(4,' ') + " PPM",  \
                              font=font, fill=255)
                    draw.text((x, top + 16), "TEM : " + "{:.1f}".format(temperature) + " C",  \
                              font=font, fill=255)
                    draw.text((x, top + 32), "HUM : " + "{:.1f}".format(humidity) + " %",  \
                              font=font, fill=255)
                    
                    print('Sleep for {0:5f} Curr Time {1}\r\n'.format((SAMPLE_TIME - (clock.now()-startTime).total_seconds()), clock.now().strftime('%x %X')))
                    
                    time.sleep(SAMPLE_TIME - (clock.now()-startTime).total_seconds())
                    
                    print('Out of sleep: {0}\r\n'.format(clock.now().strftime('%x %X')))
                    startTime = clock.now()
                    
                    draw.text((x, top + 48),  startTime.strftime('%d/%m %H:%M:%S'),  \
                              font=font, fill=255)
        
                    file.write('{0},{1:0.1f},{2:0.1f}%,{3}\r\n'.format(startTime.strftime('%x %X'),\
                                                                   temperature, humidity, Co2))
                    
                    print('{0},{1:0.1f},{2:0.1f}%,{3}, {4}\r\n'.format(startTime.strftime('%x %X'),\
                                                                   temperature, humidity, Co2, startTime.second))
        
                else:
        
                    draw.text((x, top + 0),  "Co2 : " + "ERROR",  font=font, fill=255)
                    draw.text((x, top + 16), "TEM : " + "ERROR",  font=font, fill=255)
                    draw.text((x, top + 32), "HUM : " + "ERROR",  font=font, fill=255)
            
                    startTime = clock.now()
                    draw.text((x, top + 48),  startTime.strftime('%d/%m %H:%M:%S'),  \
                              font=font, fill=255)     

                # Display image.
                disp.image(image)
                disp.display()
                time.sleep(0.1)
            
                
        except Exception as exception:
    
            print(exception)
            sys.exit(0)
        
except KeyboardInterrupt as ex:
    
    draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

    font = ImageFont.truetype('Mario-Kart-DS.ttf',24)
    draw.text((x, top + 1), "  studying ",  font=font, fill=255)
    draw.text((x, top + 22), "just  got ",  font=font, fill=255)
    draw.text((x, top + 44), "FRESHER !! ",  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)
    
    draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

    font = ImageFont.truetype('Mario-Kart-DS.ttf',34)
    draw.text((x, top + 1), "STAY ",  font=font, fill=255)
    draw.text((x, top + 33), "FRESH ! ",  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(2)
    
    disp.clear()
    disp.reset()
    disp.display()
    
    print(ex)
    
    sys.exit(0)

    
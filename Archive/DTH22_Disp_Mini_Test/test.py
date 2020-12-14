# -*- coding: cp1257 -*-

import Adafruit_DHT as tempsensor
import time
import os

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

DHT_SENSOR = tempsensor.DHT22
DHT_PIN  = 4

try:
    os.remove('testlog.csv')

except:
    pass

try:
 
    file = open('/home/pi/Study_Fresh/Archive/DTH22_Disp_Mini_Test/testlog.csv', 'a+')
    
    if os.stat('/home/pi/Study_Fresh/Archive/DTH22_Disp_Mini_Test/testlog.csv').st_size == 0:
        
        file.write('Timestamp (DD/MM/YY HH:MM:SS),Temperature (°C),Humidity (%), Co2 (ppm)\r\n')
        
except:
    pass


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(None)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline = 0, fill = 0)


# First define some constants to allow easy resizing of shapes.
padding = -1
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.truetype('04B_30.ttf',12)

draw.text((x, top + 3), "Study Fresh !",  font=font, fill=255)

font = ImageFont.truetype('04B_30.ttf',12)
draw.text((x, top + 20), "       By UQ",  font=font, fill=255)

# Display image.
disp.image(image)
disp.display()

font = ImageFont.load_default()

while True:
    
    # Get Sensor Data
    humidity, temperature = tempsensor.read_retry(DHT_SENSOR, DHT_PIN)
    Co2 = 0

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    # Write text.
    if humidity is not None and temperature is not None:
        
        draw.text((x, top),       "Temp (C)  : " + "{:.2f}".format(temperature),  font=font, fill=255)
        draw.text((x, top + 10),  "Co2  (ppm): " + str(Co2),  font=font, fill=255)
        draw.text((x, top + 24),  time.strftime('%d/%m/%y %H:%M:%S'),  font=font, fill=255)
        # Dropped Humidity
        
        file.write('{0},{1:0.1f},{2:0.1f}%,{3}\r\n'.format(time.strftime('%d/%m/%y %H:%M:%S'),temperature, humidity, str(Co2)))
        
    else:
        
        draw.text((x, top),       "Temp (C)  : " + "ERROR",  font=font, fill=255)
        draw.text((x, top + 12),  "Co2  (ppm): " + str(Co2),  font=font, fill=255)
        draw.text((x, top + 24),  time.strftime('%d/%m/%y %H:%M:%S'),  font=font, fill=255)      

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)


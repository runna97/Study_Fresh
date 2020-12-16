# -*- coding: cp1257 -*-

# Libraries for all peripherals
import Adafruit_DHT as tempsensor
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import mh_z19
import RPi.GPIO as GPIO

# Libraries for time logging 
import time
from datetime import datetime as clock
from datetime import timedelta

# Libraries for system logging
import os
import sys

# Libraries for Display
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# File import to reduce main programming visibility
import init

# DHT22 Sensor Designator
DHT_SENSOR = tempsensor.DHT22

# GPIO PIN Designator
DHT_PIN  = 4

# Nominated resolution time for storing csv data
SAMPLE_TIME = 60

# Set up the LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ledPin = 11
GPIO.setup(ledPin, GPIO.OUT)


def led_on(pin, signal):
    
    if signal == 1:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)
        
        

# Check if a file exists and create a new file
try:
    
    fileName = "./datalog.csv"
    
    led_on(ledPin, 1)
    
    if os.path.isfile(fileName):
        
        counter = 0
        
        while True:
            counter += 1
            newFileName = fileName.split(".csv")[0] + "_" + str(counter) + ".csv"
            
            # Check if the new file already exists
            if os.path.isfile(newFileName):
                
                continue
            else:
                
                fileName = newFileName
                
                break

    print('Created a new file: {0}\r'.format(fileName))
    
    file = open(fileName, 'a+')
    
    # Create headings for each file
    if os.stat(fileName).st_size == 0:
        
        file.write('Timestamp (MM/DD/YYYY HH:MM),Temperature (°C),Humidity (%),Co2 (ppm)\r\n')
        
except:
   pass


# RST varlaible for Display
RST = 24
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst = RST)

# Initialize library.
disp.begin()
disp.clear()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Draw a black filled box to clear the image.
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

# First define some constants to allow easy resizing of shapes.
padding = 1
top = padding
bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load Mario Font to 'make it fancy'.
font = ImageFont.truetype('Mario-Kart-DS.ttf',36)
draw.text((x, top + 1), "study",  font=font, fill=255)
draw.text((x, top + 33), "    fresh",  font=font, fill=255)

# Display image
disp.image(image)
disp.display()
time.sleep(1)
led_on(ledPin, 0)

# Create a blank black rectangle
draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

# Load in credits in 'fancy font'
font = ImageFont.truetype('Mario-Kart-DS.ttf',40)
draw.text((x, top + 1), "BY UQ",  font=font, fill=255)

font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf',15)
draw.text((x, top + 48), "    loading...",  font=font, fill=255)

# Display image
disp.image(image)
disp.display()

# Variable that tracks timing between samples 
startTime = clock.now()

# Variable to check if its the first loop
# First loop has a longer delay to ensure everything is initialsied during boot
tempFlag = 0

# Variables to store average values
averageHumiditySum = 0
averageTemperatureSum = 0
averageCo2Sum = 0
averageCount = 0



while True:
    
    try:
        
        
        # If first reading, keep on retrying until we get first sample
        if tempFlag is 0:
            
            humidity, temperature = tempsensor.read_retry(DHT_SENSOR, DHT_PIN)
            
        else:
            
            # If we can't get new readings in first go, assume previous
            humidity1, temperature1 = tempsensor.read(DHT_SENSOR, DHT_PIN)
            
            if humidity1 is not None and temperature1 is not None:
                
                humidity = humidity1
                temperature = temperature1
        
        # Read MH-Z19
        Co2 = mh_z19.read_all()['co2']

        # Draw a black filled box to clear the image
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        
        # Write text if we get a value from Co2 readings. 
        if Co2 is not None:
            
            # Write text onto the display
            draw.text((x, top + 0),  "Co2 : " + str(Co2).rjust(4,' ') + " PPM",  \
                      font=font, fill=255)
            draw.text((x, top + 16), "TEM : " + "{:.1f}".format(temperature) + " C",  \
                      font=font, fill=255)
            draw.text((x, top + 32), "HUM : " + "{:.1f}".format(humidity) + " %",  \
                      font=font, fill=255)
            
            # Keep track of averages
            averageHumiditySum += humidity
            averageTemperatureSum += temperature
            averageCo2Sum += Co2
            averageCount += 1
            
                        
            # If first time, go for a longer sleep
            if tempFlag == 0:
                
                # This check is to make sure we give enough time for everything to boot up
                
                sleepTime = (SAMPLE_TIME - ((clock.now() - startTime).total_seconds()))/120
                
                for i in range(0, 60):
                    
                    led_on(ledPin,1)
                    time.sleep(sleepTime)
                     
                    led_on(ledPin,0)
                    time.sleep(sleepTime)
                    
                startTime = clock.now()
                
                
            
            else:
                
                # Sleep for the 10 second increment for the display
                
                sleepTime = (10 - ((clock.now() - startTime).total_seconds()))/20
                
                for i in range(0, 10):
                     
                    led_on(ledPin,1)
                    time.sleep(sleepTime)
                     
                    led_on(ledPin,0)
                    time.sleep(sleepTime)
                    
                startTime = startTime + timedelta(seconds = 10)
            
            # Depending on the delay, write text on the display
            draw.text((x, top + 48),  startTime.strftime('%d/%m %H:%M:%S'),  \
                      font=font, fill=255)
            
            print('Current: {0}, {1:0.1f} C, {2:0.1f} %, {3} ppm \r'.format(startTime.strftime('%x %X'),\
                                                                           temperature, humidity, Co2,))            
            
            # If we are ready to count average or if its the first reading
            if averageCount == 6 or tempFlag == 0:
                
                # Write and sync to file to sure data is safely stored 
                file.write('{0},{1:0.1f},{2:0.1f}%,{3:.2f}\r\n'.format(startTime.strftime('%x %X'),\
                                                                       (averageTemperatureSum/averageCount), \
                                                                       (averageHumiditySum/averageCount), \
                                                                       (averageCo2Sum/averageCount)))
                file.flush()
                os.fsync(file)
                
                print('\nAverage: {0}, {1:0.1f} C, {2:0.1f} %, {3:.0f} ppm \r\n'.format(startTime.strftime('%x %X'),\
                                                                       (averageTemperatureSum/averageCount), \
                                                                       (averageHumiditySum/averageCount), \
                                                                       (averageCo2Sum/averageCount)))
                
                # Reset all average values and raise flag for 10 second readings
                averageHumiditySum = averageTemperatureSum = averageCo2Sum = averageCount = 0
                tempFlag = 1
        
        else:
            
            # If any errors in readings display ERROR
            draw.text((x, top + 0),  "Co2 : " + "ERROR",  font=font, fill=255)
            draw.text((x, top + 16), "TEM : " + "ERROR",  font=font, fill=255)
            draw.text((x, top + 32), "HUM : " + "ERROR",  font=font, fill=255)
            
            startTime = clock.now()
            draw.text((x, top + 48),  startTime.strftime('%d/%m %H:%M:%S'),  \
                      font=font, fill=255)     

        # Display image.
        disp.image(image)
        disp.display()

    # If any unwanted exceptions
    except Exception as exception:
    
        led_on(ledPin, 1)
        time.sleep(1)
        led_on(ledPin, 0)
        
        print(exception)
        sys.exit(0)
     
    # For Keyboard interrupts
    except KeyboardInterrupt as ex:
        
        led_on(ledPin, 1)
        
        print("\n Preparing to close application. Please wait for 3 seconds...\n")
        
        # Create black display
        draw.rectangle((0, 0, width, height), outline = 0, fill = 0)
        
        # Say a 'cringeworthy phrase'
        font = ImageFont.truetype('Mario-Kart-DS.ttf',24)
        draw.text((x, top + 1), "  studying ",  font=font, fill=255)
        draw.text((x, top + 22), "just  got ",  font=font, fill=255)
        draw.text((x, top + 44), "FRESHER !! ",  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(2)
        
        # Create black display
        draw.rectangle((0, 0, width, height), outline = 0, fill = 0)

        # Say bye to the kids
        font = ImageFont.truetype('Mario-Kart-DS.ttf',34)
        draw.text((x, top + 1), "STAY ",  font=font, fill=255)
        draw.text((x, top + 33), "FRESH ! ",  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(2)
    
        # Rest display for proper shutdown
        disp.clear()
        disp.reset()
        disp.display()
        
        # Close csv file
        file.close()
        
        print("All done!")
        print("Byeee! Stay Fresh!")
        
        led_on(ledPin, 0)

        print(ex)
        sys.exit(0)
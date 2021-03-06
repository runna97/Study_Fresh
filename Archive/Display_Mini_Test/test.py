
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(None)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

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
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.truetype('04B_30.ttf',12)

draw.text((x, top + 20), "Study Fresh!!",  font=font, fill=255)

# Display image.
disp.image(image)
disp.display()
time.sleep(2) 

# Clear display.
disp.clear()
disp.display()

font = ImageFont.load_default()

while True:




    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    # Write text.

    draw.text((x, top),       "Temp (C)  : " + str(0),  font=font, fill=255)
    draw.text((x, top + 12),  "Hum  (%)  : " + str (0), font=font, fill=255)
    draw.text((x, top + 24),  "Co2  (ppm): " + str(0),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)


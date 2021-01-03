# Libraries for all peripherals
import Adafruit_SSD1306

# Libraries for Display
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# RST varlaible for Display
RST = 24


class DisplayScreen:
	def __init__(self):
	
		# 128x64 display with hardware I2C:
		self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

		# Initialize library.
		self.disp.begin()
		self.disp.clear()

		# Create blank image for drawing.
		# Make sure to create image with mode '1' for 1-bit color.
		self.width = self.disp.width
		self.height = self.disp.height
		self.image = Image.new('1', (self.width, self.height))

		# Draw a black filled box to clear the image.
		self.draw = ImageDraw.Draw(self.image)
		self.blank()

		# First define some constants to allow easy resizing of shapes.
		self.padding = 1
		self.top = self.padding
		self.bottom = self.height - self.padding

		# Move left to right keeping track of the current x position for drawing
		# shapes.
		self.x= 0
		
	def blank(self):
		
		# Draw a black filled box to clear the image
		self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
	def write(self, position, text):
		
		self.draw.text((self.x, self.top + position), text, font=self.font, fill=255)

	def loading_screen(self):
		
		# Load Mario Font to 'make it fancy'.
		self.font = ImageFont.truetype('Mario-Kart-DS.ttf', 36)
		self.write(1 , "study")
		self.write(33, "    fresh")

		# Display image
		self.disp.image(self.image)
		self.disp.display()	
		
	def opening_credits(self):
		
		# Create a blank black rectangle
		self.blank()

		# Load in credits in 'fancy font'
		self.font = ImageFont.truetype('Mario-Kart-DS.ttf', 40)
		self.write(1, "BY UQ")

		self.font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 15)
		self.write(48, "    loading...")

		# Display image
		self.disp.image(self.image)
		self.disp.display()
			
	def closing_remarks(self):
				
		# Create a blank black rectangle
		self.blank()

		# Say a 'cringeworthy phrase'
		self.font = ImageFont.truetype('Mario-Kart-DS.ttf', 24)
		self.write(1, "  studying ")
		self.write(22, "just  got ")
		self.write(44, "FRESHER !! ")

		# Display image.
		self.disp.image(self.image)
		self.disp.display()
	
	def goodbye(self):
		
		# Create a blank black rectangle
		self.blank()

		# Say bye to the kids
		self.font = ImageFont.truetype('Mario-Kart-DS.ttf', 34)

		self.write(1, "STAY ")
		self.write(33, "FRESH ! ")
		
		# Display image.
		self.disp.image(self.image)
		self.disp.display()
        
	def shutdown(self):

		# Rest display for proper shutdown
		self.disp.clear()
		self.disp.reset()
		self.disp.display()
		
	def flush(self):
		
		self.disp.image(self.image)
		self.disp.display()
	

# Libraries for all peripherals
#import RPi.GPIO as GPIO
from gpiozero import LED

# Set up the LED with GPIO designators
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)


class LedArray:
	
	def __init__(self,redLED, yellowLED, greenLED):
		
		self.redLED = redLED
		self.yellowLED = yellowLED
		self.greenLED  = greenLED

		self.redLED.off()
		self.yellowLED.off()
		self.greenLED.off()

		
	def light(self,led, signal):
		
		
		if signal == 1:
			led.on()
		else:
			led.off()
	
	def light_duo(self, ledOne, ledTwo, signal):
		
		if signal == 1:
			ledOne.on()
			ledTwo.on()
		else:
			ledOne.off()	
			ledTwo.off()
			
	def light_all(self, signal):
		
		if signal == 1:
			
			self.redLED.on()
			self.yellowLED.on()
			self.greenLED.on()
			
		else:
			
			self.redLED.off()
			self.yellowLED.off()
			self.greenLED.off()



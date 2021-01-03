# Libraries for all peripherals
import mh_z19

class CO2Sensor:
	def __init__(self):
		
		self.Co2 = 0
		
	def read(self):
		
		try:
			
			self.Co2 = mh_z19.read_all()['co2']
			
		except:
			
			self.Co2 = 0
			pass
		
		return self.Co2


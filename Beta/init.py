###################################################################
#
#   Study Fresh Project - Monitoring Program
#
#   Using Citizen Science to Engage Children with Indoor Air Quality
#
#   Recipient of Queensland Citizen Science Grant from 
#   Queensland Department of Environment and Science
# 
#   Project Lead: Dr Steven Snow
#
#   Project Members: Dr Lisa Ottenhaus, Dr Mashhuda Glencross
#                    Dr Paola Leardini, Brett Beeson, 
#                    Rohith Nunna
#
###################################################################

###################################################################
# Intialize all peripherals for Study Fresh Project
###################################################################

# Import Peripherals

from peripherals.tempsensor import *
from peripherals.co2 import*
from peripherals.display import *
from peripherals.led import*

# Libraries for time logging
import time
from datetime import datetime as clock
from datetime import timedelta

# Libraries for system logging
import os
import sys

# Nominated resolution time for storing csv data
SAMPLE_TIME = 60

class Logger:
	""" Class designed to log sensor values to a .csv file
	
	"""

	def __init__(self, fileName):
		
		self.fileName = fileName
		if os.path.isfile(self.fileName):

			self.counter = 0

			while True:
				self.counter += 1
				self.newFileName = self.fileName.split(
					".csv")[0] + "_" + str(self.counter) + ".csv"

				# Check if the new file already exists
				if os.path.isfile(self.newFileName):

					continue
				else:

					self.fileName = self.newFileName

					break

		print('Created a new file: {0}\r'.format(self.fileName))
	
		#self.filename = filename
		self.file = open(self.fileName, 'a+')

		# Create headings for each file
		if os.stat(self.fileName).st_size == 0:

			self.file.write(
				'Timestamp (MM/DD/YYYY HH:MM),Temperature (°C),'
				'Humidity (%),Co2 (ppm)\r\n')
				
	def log(self, text):
		
		self.file.write(text)
		self.file.flush()
		os.fsync(self.file)
		
		
	def exit(self):
		self.file.close()

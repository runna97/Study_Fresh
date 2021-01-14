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

###################################################################
# File Imports
###################################################################
# Importing temperature sensor
from peripherals.tempsensor import *

# Importing CO2 sensor
from peripherals.co2 import*

# Importing Display module
from peripherals.display import *

# Importing LEDs as a single module
from peripherals.led import*

# Libraries for time logging
import time
from datetime import datetime as clock
from datetime import timedelta

# Libraries for system logging
import os
import sys

###################################################################
# Global Variables
###################################################################
# Nominated resolution time for storing csv data
SAMPLE_TIME = 60

# Defines the pin for the temperature sensor
DHT_PIN = 4

###################################################################
# Global Classes
###################################################################

class Logger:

    """
        Purpose: Class for logging sensor values to a .csv file
        Inputs:  None
        Outputs: None
    """

    def __init__(self, fileName):
        """
            Purpose: Initializing the new file by the filename given
            Inputs:  filename is the nominated name for data logger
            Outputs: None
        """

        self.fileName = fileName

        # Check if the file already exists
        if os.path.isfile(self.fileName):

            self.counter = 0

            # If it does keep counting until a unique file is found
            while True:

                self.counter += 1
                self.newFileName = self.fileName.split(
                        ".csv")[0] + "_" + str(self.counter) + ".csv"

                # Check if the new file already exists
                if os.path.isfile(self.newFileName):

                    continue
                else:

                    # The unique file is found, so break up
                    self.fileName = self.newFileName
                    break

        print('Created a new file: {0}\r'.format(self.fileName))

        # open the file name to store data
        self.file = open(self.fileName, 'a+')

        # Create a header row if file is empty
        if os.stat(self.fileName).st_size == 0:

            self.file.write(
                    'Timestamp (MM/DD/YYYY HH:MM),Temperature (°C),'
                    'Humidity (%),Co2 (ppm)\r\n')

    def log(self, text):

        """
            Purpose: Function to write text to .csv
            Inputs:  text is the string in the .csv
            Outputs: None
        """

        self.file.write(text)
        self.file.flush()
        os.fsync(self.file)

    def exit(self):

        """
            Purpose: Close the file
            Inputs:  None
            Outputs: None
        """

        self.file.close()


# Class to manager the CO2 Sensor
co2Sensor = CO2Sensor()

# Class to manage the SD Card
excelFile = Logger("./datalog.csv")

# Class to manager the Display
screen = DisplayScreen()

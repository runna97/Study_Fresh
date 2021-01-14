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

# Defines the pin for the temperature sensor
DHT_PIN = 4

###################################################################
# Global Classes
###################################################################

# Class to manager the CO2 Sensor
co2Sensor = CO2Sensor()

# Class to manager the Display
screen = DisplayScreen()

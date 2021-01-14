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
# Peripheral File for RGB LED Scheme
###################################################################

###################################################################
# File Imports
###################################################################

# GPIO Library for LED
from gpiozero import LED

###################################################################
# Global Classes
###################################################################
class LedArray:

    """
        Purpose: Class to manage the RYB LEDs
        Inputs:  None
        Outputs: None
    """

    def __init__(self, redLED, yellowLED, greenLED):

        """
            Purpose: Initialise the LEDs
            Inputs:  redLED, yellowLED and greenLED
            Outputs: None
        """

        self.redLED = redLED
        self.yellowLED = yellowLED
        self.greenLED = greenLED

        self.redLED.off()
        self.yellowLED.off()
        self.greenLED.off()

    def write(self, led, signal):

        """
            Purpose: Toggle the LED based on the signal
            Inputs:  led is the required LED
             signal is the binary signal
            Outputs: None
        """

        if signal == 1:
            led.on()
        else:
            led.off()

    def write_duo(self, ledOne, ledTwo, signal):

        """
            Purpose: Toggle two LEDs based on the signal
            Inputs:  ledOne is the required LED
                     ledTwo is the second LED       
                     signal is the binary signal
            Outputs: None
        """

        if signal == 1:
            ledOne.on()
            ledTwo.on()
        else:
            ledOne.off()
            ledTwo.off()

    def write_all(self, signal):

        """
            Purpose: Toggle two LEDs based on the signal
            Inputs:  signal is the binary signal
            Outputs: None
        """

        if signal == 1:

            self.redLED.on()
            self.yellowLED.on()
            self.greenLED.on()

        else:

            self.redLED.off()
            self.yellowLED.off()
            self.greenLED.off()


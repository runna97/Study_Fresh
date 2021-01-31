#! /usr/bin/python3

###################################################################
# BLINK test program
#
# Turns an LED on for one second, then off for another, repeatedly
#
###################################################################

###################################################################
# File Imports _ DO NOT MODIFY
###################################################################
# General Purpose Input/ Output (GPIO) Library for LED
from gpiozero import LED

import time

###################################################################
# Global Variables - DO NOT MODIFY
###################################################################

# Defines the pin for the green LED
greenLED = LED(26)

###################################################################
# Functions - DO NOT MODIFY
###################################################################


def setup():
    """
        Purpose: Ensures all components are installed correctly
        Inputs:  None
        Outputs: None
    """
    greenLED.off()  


###################################################################
# Main Function - DO NOT MODIFY
###################################################################


def main():
    """
        Purpose: Main loop that coordinates the sampling forever
        Inputs:  None
        Outputs: None
    """
    # Light up green LED
    greenLED.on()
    
    time.sleep(5)



###################################################################
# Compiler Code - DO NOT MODIFY
###################################################################

if __name__ == '__main__':

    setup()
    main()


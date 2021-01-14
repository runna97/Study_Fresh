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

# Importing time module to wait during commands
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
    # Wait for 1 second
    time.sleep(1)

    # Shut down green LED
    greenLED.off()
    # Wait for 1 second
    time.sleep(1)



###################################################################
# Compiler Code - DO NOT MODIFY
###################################################################

if __name__ == '__main__':

    setup()
    try:
        
        while True:
            main()

    # For Keyboard interrupts
    except KeyboardInterrupt as ex:

        greenLED.off()
        print("Exiting blink program now")
        print("Byeeee!!!!!")

        print(ex)

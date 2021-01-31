#! /usr/bin/python3
# -*- coding: cp1257 -*-

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
# Main Python Program File for Study Fresh Monitoring Project
###################################################################

###################################################################
# File Imports - DO NOT MODIFY
###################################################################
# Importing Peripherals required for the project
from init import *

###################################################################
# Global Variables - DO NOT MODIFY
###################################################################

# Defines the pin for the red LED
redLED = LED(13)

# Defines the pin for the yellow LED
yellowLED = LED(19)

# Defines the pin for the green LED
greenLED = LED(26)

###################################################################
# Functions
###################################################################


def setup():
    """
        Purpose: Ensures all components are installed correctly
        Inputs:  None
        Outputs: None
    """

    screen.loading_screen()
    time.sleep(1)
    screen.opening_credits()


def ledSelect(Co2, sleepTime):
    """
        Purpose: Select the correct LED based on CO2 readings
        Inputs:  Co2 is the value returned from the CO2 sensor
                 sleepTime is the time require to hold LED at a level
        Outputs: None
    """

    """
        STAGE 1: Set all the LEDs off using ___.off()
    """

    greenLED.off()
    # Turn off yellow LED
    # Turn off red LED

    """
        END CODE FOR STAGE 1
    """

    """
        STAGE 2: Using if-else(), turn on the LEDs based on CO2 values:
        Red    -> when CO2 level is greater than or equal to 1200
        Yellow -> when CO2 level is greater than or equal to 800 but less than 1200
        Green  -> when CO2 level is less than 800
    """

    # Change the values to the correct CO2 Levels
    dangerLevel = 0
    warningLevel = 0

    if Co2 >= dangerLevel:

        # Replace below line turn on the red LED
        greenLED.on()

    elif Co2 >= warningLevel:

        # Replace below line turn on the yellow LED
        greenLED.on()
        
    else:

        greenLED.on()

    # Hold LED value for 100 milliseconds
    time.sleep(sleepTime)


###################################################################
# Main Loop - DO NOT MODIFY
###################################################################

def main():
    """
        Purpose: Main loop that coordinates the sampling forever
        Inputs:  None
        Outputs: None
    """

    try:

        # Get Humidity and Temperature fromse sensor
        humidity, temperature = tempsensor.read_retry(
            DHT_SENSOR, DHT_PIN)

        # Get CO2 from sensor
        Co2 = co2Sensor.read()

        # Clear screen first
        screen.blank()

        # Write text if we get a value from Co2 readings.
        if Co2 is not None:

            # Write text onto the display
            screen.write(0, "Co2 : " + str(Co2).rjust(4, ' ')
                         + " PPM")

            screen.write(16, "TEM : " + "{:.1f}".format(temperature)
                         + " C")

            screen.write(32, "HUM : {:.1f}".format(humidity) +
                         " %")

            ledSelect(Co2, 0.1)

            # Clock the timestamp
            startTime = clock.now()

            # Depending on the delay, write text on the display
            screen.write(48, startTime.strftime('%d/%m %H:%M:%S'))

            # Print onto the terminal
            print('Time: {0}  Temperature: {1:0.1f} C  Humidity: {2:0.1f} %  CO2: {3} ppm  \r'.format(
                startTime.strftime('%x %X'), temperature, humidity, Co2,))

        else:

            # If any errors in readings display ERROR
            screen.write(0, "Co2 : " + "ERROR")
            screen.write(16, "TEM : " + "ERROR")
            screen.write(32, "HUM : " + "ERROR")
            screen.write(48, startTime.strftime('%d/%m %H:%M:%S'))

        screen.flush()

    # If any unwanted exceptions
    except Exception as exception:

        greenLED.on()
        yellowLED.on()
        redLED.on()

        time.sleep(1)

        greenLED.off()
        yellowLED.off()
        redLED.off()

        print(exception)
        sys.exit(0)

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

        greenLED.on()
        yellowLED.on()
        redLED.on()

        print("\n Preparing to close application. Please wait for 3 seconds...\n")

        screen.closing_remarks()
        time.sleep(1.5)

        screen.goodbye()
        time.sleep(1.5)

        screen.shutdown()

        print("All done!")
        print("Byeee! Stay Fresh!")

        greenLED.off()
        yellowLED.off()
        redLED.off()

        print(ex)
        sys.exit(0)

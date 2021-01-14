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
# Main Python Program File for Study Fresh Project
###################################################################

###################################################################
# File Imports
###################################################################
# Importing Peripherals required for the project
from init import *

###################################################################
# Global Variables
###################################################################
# Defines the pin for the temperature sensor
DHT_PIN = 4
# Defines the pin for the red LED
redLED = LED(13)
# Defines the pin for the yellow LED
yellowLED = LED(19)
# Defines the pin for the green LED
greenLED = LED(26)

###################################################################
# Global Classes
###################################################################
# Class to manager the CO2 Sensor
co2Sensor = CO2Sensor()
# Class to manage the SD Card
excelFile = Logger("./datalog.csv")
# Class to manager the Display
screen = DisplayScreen()
# Class to manager the LED
leds = LedArray(redLED, yellowLED, greenLED)

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


def select(Co2, sleepTime):
    """
        Purpose: Select the correct LED based on CO2 readings
        Inputs:  Co2 is the value returned from the CO2 sensor
                 sleepTime is the time require to hold LED at a level
        Outputs: None
    """

    dangerLevel = 1200
    warningLevel = 800

    # If CO2 is greater than danger level,
    # light every LED

    if Co2 >= dangerLevel:

        # Light up all LEDs
        leds.light_all(1)
        time.sleep(sleepTime)

        # Shut down all LEDs
        leds.light_all(0)
        time.sleep(sleepTime)

    # If CO2 is greater than the warning level,
    # light green and yellow LED
    elif Co2 >= warningLevel:

        # Light up green and yellow LED
        leds.light_duo(greenLED, yellowLED, 1)
        time.sleep(sleepTime)

        # Shut down green and yellow LED
        leds.light_duo(greenLED, yellowLED, 0)
        time.sleep(sleepTime)

    # If CO2 level is below the warning level,
    # light up green LED
    else:

        # Light up green LED
        leds.light(greenLED, 1)
        time.sleep(sleepTime)

        # Shut down green LED
        leds.light(greenLED, 0)
        time.sleep(sleepTime)

###################################################################
# Main Loop
###################################################################


def main():
    """
        Purpose: Main loop that coordinates the sampling forever
        Inputs:  None
        Outputs: None
    """

    # Variable to check if we can get a valid reading
    tempFlag = 0

    # Variables to store average values
    averageHumiditySum = 0
    averageTemperatureSum = 0
    averageCo2Sum = 0
    # Variable to store the count for samples
    averageCount = 0

    # Variable that tracks timing between samples
    startTime = clock.now()

    # First loop that gets readings and samples accordingly
    while True:

        try:

            # If first temp reading,
            # keep on retrying until we get first sample
            if tempFlag is 0:

                humidity, temperature = tempsensor.read_retry(
                    DHT_SENSOR, DHT_PIN)

            else:

                # If we can't get new reading, assume previous
                humidity1, temperature1 = tempsensor.read(
                    DHT_SENSOR, DHT_PIN)

                if humidity1 is not None and temperature1 is not None:

                    humidity = humidity1
                    temperature = temperature1

            # Read MH-Z19
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

                # Keep track of averages
                averageHumiditySum += humidity
                averageTemperatureSum += temperature
                averageCo2Sum += Co2
                averageCount += 1

                # If first time, go for a longer sleep
                if tempFlag == 0:

                    # This check is to buffer load time for first read

                    sleepTime = (SAMPLE_TIME -
                                 ((clock.now() - startTime).total_seconds())) / 120

                    # This loop ensures we blink 60 times for loadup
                    for i in range(0, 60):

                        select(Co2, sleepTime)

                    startTime = clock.now()

                else:

                    # Sleep for the 10 second increment for the display
                    sleepTime = (
                        10 - ((clock.now() - startTime).total_seconds())) / 20

                    # Blink for 10 times
                    for i in range(0, 10):

                        select(Co2, sleepTime)

                    startTime = startTime + timedelta(seconds=10)

                # Depending on the delay, write text on the display
                screen.write(48, startTime.strftime('%d/%m %H:%M:%S'))

                # Print onto the terminal
                print('Current: {0}, {1:0.1f} C, {2:0.1f} %, {3} ppm \r'.format(
                    startTime.strftime('%x %X'), temperature, humidity, Co2,))

                # If we are ready to count average or if its the first reading
                if averageCount == 6 or tempFlag == 0:

                    # Write and sync to file to sure data is safely stored
                    excelFile.log(
                        '{0},{1:0.1f},{2:0.1f}%,{3:.2f}\r\n'.format(
                            startTime.strftime('%x %X'),
                            (averageTemperatureSum / averageCount),
                            (averageHumiditySum / averageCount),
                            (averageCo2Sum / averageCount)))

                    print(
                        '\nAverage: {0}, {1:0.1f} C, {2:0.1f} %, {3:.0f} ppm \r\n'.format(
                            startTime.strftime('%x %X'),
                            (averageTemperatureSum / averageCount),
                            (averageHumiditySum / averageCount),
                            (averageCo2Sum / averageCount)))

                    # Reset all average values and raise flag for 10 second
                    # readings
                    averageHumiditySum = averageTemperatureSum = averageCo2Sum = averageCount = 0
                    tempFlag = 1

            else:

                # If any errors in readings display ERROR
                screen.write(0, "Co2 : " + "ERROR")
                screen.write(16, "TEM : " + "ERROR")
                screen.write(32, "HUM : " + "ERROR")

                startTime = clock.now()
                screen.write(48, startTime.strftime('%d/%m %H:%M:%S'))

            screen.flush()

        # If any unwanted exceptions
        except Exception as exception:

            leds.light_all(1)

            time.sleep(1)

            leds.light_all(0)

            print(exception)
            sys.exit(0)


if __name__ == '__main__':

    setup()

    try:
        main()

    # For Keyboard interrupts
    except KeyboardInterrupt as ex:

        leds.light_all(1)

        print("\n Preparing to close application. Please wait for 3 seconds...\n")

        screen.closing_remarks()
        time.sleep(1.5)

        screen.goodbye()
        time.sleep(1.5)

        screen.shutdown()

        # Close csv file
        excelFile.exit()

        print("All done!")
        print("Byeee! Stay Fresh!")

        leds.light_all(0)

        print(ex)
        sys.exit(0)

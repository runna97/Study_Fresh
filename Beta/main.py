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
#s
#   Project Members: Dr Lisa Ottenhaus, Dr Mashhuda Glencross
#                    Dr Paola Leardini, Brett Beeson, 
#                    Rohith Nunna
#
###################################################################

###################################################################
# Main Python Program File for Study Fresh Project
###################################################################

# File import to reduce main programming visibility
from init import *

# GPIO PIN Designator
DHT_PIN = 4
greenLed = 26
yellowLED = 19
redLED = 13

excelFile = Logger("./datalog.csv")
screen = DisplayScreen()

def setup():
    
    GPIO.setup(greenLed, GPIO.OUT)
    GPIO.setup(yellowLED, GPIO.OUT)
    GPIO.setup(redLED, GPIO.OUT)

    screen.loading_screen()
    
    led_on(greenLed, 0)
    
    screen.opening_credits()

#setup()

def main():
        
    # Variable to check if its the first loop
    # First loop has a longer delay to ensure everything is initialsied during boot
    tempFlag = 0
    
    # Variables to store average values
    averageHumiditySum = 0
    averageTemperatureSum = 0
    averageCo2Sum = 0
    averageCount = 0
    
    # Variable that tracks timing between samples
    startTime = clock.now()
    
    while True:
    
        try:
    
            # If first reading, keep on retrying until we get first sample
            if tempFlag is 0:
    
                humidity, temperature = tempsensor.read_retry(DHT_SENSOR, DHT_PIN)
    
            else:
    
                # If we can't get new readings in first go, assume previous
                humidity1, temperature1 = tempsensor.read(DHT_SENSOR, DHT_PIN)
    
                if humidity1 is not None and temperature1 is not None:
    
                    humidity = humidity1
                    temperature = temperature1
    
            # Read MH-Z19
            Co2 = mh_z19.read_all()['co2']
    
            screen.blank()
    
            # Write text if we get a value from Co2 readings.
            if Co2 is not None:
    
                # Write text onto the display
                screen.write(0, "Co2 : " + str(Co2).rjust(4, ' ') + " PPM")
                screen.write(16, "TEM : " + "{:.1f}".format(temperature) + " C")
                screen.write(32, "HUM : {:.1f}".format(humidity) + " %")
    
                # Keep track of averages
                averageHumiditySum += humidity
                averageTemperatureSum += temperature
                averageCo2Sum += Co2
                averageCount += 1
    
                # If first time, go for a longer sleep
                if tempFlag == 0:
    
                    # This check is to make sure we give enough time for everything
                    # to boot up
    
                    sleepTime = (
                        SAMPLE_TIME - ((clock.now() - startTime).total_seconds())) / 120
    
                    for i in range(0, 60):
    
                        if Co2 >= 1000:
    
                            led_on(greenLed, 1)
                            led_on(yellowLED, 1)
                            led_on(redLED, 1)
    
                            time.sleep(sleepTime)
    
                            led_on(greenLed, 0)
                            led_on(yellowLED, 0)
                            led_on(redLED, 0)
    
                            time.sleep(sleepTime)
    
                        elif Co2 >= 800:
    
                            led_on(greenLed, 1)
                            led_on(yellowLED, 1)
    
                            time.sleep(sleepTime)
    
                            led_on(greenLed, 0)
                            led_on(yellowLED, 0)
    
                            time.sleep(sleepTime)
    
                        else:
                            led_on(greenLed, 1)
    
                            time.sleep(sleepTime)
    
                            led_on(greenLed, 0)
    
                            time.sleep(sleepTime)
    
                    startTime = clock.now()
    
                else:
    
                    # Sleep for the 10 second increment for the display
    
                    sleepTime = (
                        10 - ((clock.now() - startTime).total_seconds())) / 20
    
                    for i in range(0, 10):
    
                        if Co2 >= 1000:
    
                            led_on(greenLed, 1)
                            led_on(yellowLED, 1)
                            led_on(redLED, 1)
    
                            time.sleep(sleepTime)
    
                            led_on(greenLed, 0)
                            led_on(yellowLED, 0)
                            led_on(redLED, 0)
    
                            time.sleep(sleepTime)
    
                        elif Co2 >= 800:
    
                            led_on(greenLed, 1)
                            led_on(yellowLED, 1)
    
                            time.sleep(sleepTime)
    
                            led_on(greenLed, 0)
                            led_on(yellowLED, 0)
    
                            time.sleep(sleepTime)
    
                        else:
                            led_on(greenLed, 1)
    
                            time.sleep(sleepTime)
    
                            led_on(greenLed, 0)
    
                            time.sleep(sleepTime)
    
                    startTime = startTime + timedelta(seconds=10)
    
                # Depending on the delay, write text on the display
                screen.write(48, startTime.strftime('%d/%m %H:%M:%S'))
    
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

            led_on(redLED, 1)
            led_on(greenLed, 1)
            led_on(yellowLED, 1)
    
            time.sleep(1)
            led_on(redLED, 0)
            led_on(greenLed, 0)
            led_on(yellowLED, 0)
    
            print(exception)
            sys.exit(0)


if __name__ == '__main__':
    
    setup()
    
    try:
        main()
    
    # For Keyboard interrupts
    except KeyboardInterrupt as ex:

        led_on(redLED, 1)
        led_on(greenLed, 1)
        led_on(yellowLED, 1)
    
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
    
        led_on(redLED, 0)
        led_on(greenLed, 0)
        led_on(yellowLED, 0)
    
        print(ex)
        sys.exit(0)
    

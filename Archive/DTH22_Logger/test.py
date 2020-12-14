# -*- coding: cp1257 -*-

import Adafruit_DHT as tempsensor
import time
import os

DHT_SENSOR = tempsensor.DHT22
DHT_PIN  = 4

try:
    file = open('/home/pi/Study_Fresh/DTH22_Logger/test.csv', 'a+')
    
    if os.stat('/home/pi/Study_Fresh/DTH22_Logger/test.csv').st_size == 0:
        
        file.write('Timestamp (DD/MM/YY HH:MM:SS),Temperature (°C),Humidity (%)\r\n')
        
except:
    pass

try:
    while True:
        
        humidity, temperature = tempsensor.read_retry(DHT_SENSOR, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            
            file.write('{0},{1:0.1f},{2:0.1f}%\r\n'.format(time.strftime('%d/%m/%y %H:%M:%S'),temperature, humidity))
            print("{0}: Temperature = {1:0.1f} C  Humidity = {2:0.1f} %".format(time.strftime('%d/%m/%y %H:%M:%S'),temperature, humidity))
            
        else:
                
            print("Error")
        
        time.sleep(3)
    
except KerboardInterrupt:
    pass
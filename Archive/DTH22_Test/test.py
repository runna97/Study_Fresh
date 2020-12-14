import Adafruit_DHT as tempsensor
import time

DHT_SENSOR = tempsensor.DHT22
DHT_PIN  = 4

while True:
    
    humidity, temperature = tempsensor.read_retry(DHT_SENSOR, DHT_PIN)
    
    if humidity is not None and temperature is not None:
        print("Date = {0} Time = {1} Temperature = {2:0.1f} C   Humidity = {3:0.1f} %".format(time.strftime('%d/%m/%y'),time.strftime('%H:%M:%S'),temperature, humidity))

    else:
        print("Error")
        
    time.sleep(3)

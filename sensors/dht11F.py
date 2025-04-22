import Freenove_DHT as DHT
import RPi.GPIO as GPIO
import time

DHTPin = 18 

def get_temperature():
    dht = DHT.DHT(DHTPin)
    for _ in range(15):  
        if dht.readDHT11() == 0:  
            return round(dht.getTemperature(), 2)
        time.sleep(0.1)
    return None  

def get_humidity():
    dht = DHT.DHT(DHTPin)
    for _ in range(15):  
        if dht.readDHT11() == 0:  
            return round(dht.getHumidity(), 2)
        time.sleep(0.1)
    return None  

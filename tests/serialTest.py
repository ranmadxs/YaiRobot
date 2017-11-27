'''
Created on 23-11-2017

@author: instala
'''
import serial
import time
ser = serial.Serial('COM4', 9600, timeout=0)
ser.write("Init")
var = raw_input("Enter something: ")
#ser.write("SERIAL,SERVO,ANGLE,S3003,9,50,0,None,None")
ser.write(var)
while 1:
    try:
        print ser.readline()
        time.sleep(1)
    except ser.SerialTimeoutException:
        print('Data could not be read')
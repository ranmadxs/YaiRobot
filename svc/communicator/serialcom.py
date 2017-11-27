'''
Created on 29-10-2017

@author: esanchez
'''
from lib.logger import logger as log
from exception import YaiRoverException
from enumrobot.serial import SerialEnum
import serial
import time

class YaiSerialSvc():
    
        
    SERIAL_BAUD_RATE = 9600
    def __init__(self):
        self.arduino = serial.Serial("COM4", self.SERIAL_BAUD_RATE)
        self.arduino.write("init")


    def sendCommand(self, strSend, port = SerialEnum.SERIAL_TTYS1_PORT.value, baud = SERIAL_BAUD_RATE):
        log.debug(">> %s" % strSend)
        #arduino = serial.Serial(port, baud)
        sendCmd = strSend.encode('utf-8')
        self.arduino.write(sendCmd)
        time.sleep(2)
        #Esto lee todas la lineas
        msg = self.arduino.read(self.arduino.inWaiting())
        log.debug("<< %s" % msg)
                
        return msg
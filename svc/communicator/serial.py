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

    def sendCommand(self, strSend, port = SerialEnum.SERIAL_TTYS1_PORT.value, baud = SERIAL_BAUD_RATE):
        log.debug(">> %s" % strSend)
        arduino = serial.Serial(port, baud)
        sendCmd = strSend.encode('utf-8')
        arduino.write(sendCmd)
        time.sleep(2)
        #Esto lee todas la lineas
        msg = arduino.read(arduino.inWaiting())
        log.debug("<< %s" % msg)
                
        return msg
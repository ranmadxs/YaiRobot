'''
Created on 29-10-2017

@author: esanchez
'''

import smbus
import time
from lib.logger import logger as log
from exception import YaiRoverException

class I2CSvc():
    
    MAX_I2C_COMAND = 32
    MAX_I2C_CONTENT = 26
    I2C_DEV = 0
    YAI_COMMAND_TYPE_I2C = "I2C"
    
    def StringToBytes(self, val):
        retVal = []
        for c in val:
                retVal.append(ord(c))
        return retVal
    
    def buildI2Cpackage(self, command, total, part) :
        respCommand = "%s%s%s%s" % (self.YAI_COMMAND_TYPE_I2C, part, total, command);
        return respCommand

    def sendCommand(self, cmd, clientAddres = None):   
        
        if clientAddres is None:
            raise YaiRoverException("clientAddres no puede ser nulo")        
             
        bus = smbus.SMBus(self.I2C_DEV)
        log.info(" >> %s" % cmd)
        totalParts = 1;
        if (len(cmd) > self.MAX_I2C_CONTENT) :
            totalParts = 2;
        cmd1 = cmd[:self.MAX_I2C_CONTENT]
        #print cmd1
        cmd1 = self.buildI2Cpackage(cmd1, totalParts, 1)
        log.debug("[p1]>>" + cmd1)
        messageInBytes = self.StringToBytes(cmd1)
        bus.write_i2c_block_data(clientAddres, 0, messageInBytes)
        
        #data_received_from_Arduino = bus.read_i2c_block_data(clientAddres, 0,32)
        #print(data_received_from_Arduino)
        time.sleep(.25)
        if (totalParts > 1) :
            cmd2 = cmd[self.MAX_I2C_CONTENT:]
            #print cmd2
            cmd2 = self.buildI2Cpackage(cmd2, totalParts, 2)
            log.debug("[p2]>>" + cmd2)
            messageInBytes = self.StringToBytes(cmd2)
            bus.write_i2c_block_data(clientAddres, 0, messageInBytes)
        
        time.sleep(0.2)        
        smsMessage = ""
        data_received_from_Arduino = bus.read_i2c_block_data(clientAddres, 0,32)
        for i in range(len(data_received_from_Arduino)):
            smsMessage += chr(data_received_from_Arduino[i])
        
        log.debug(data_received_from_Arduino) 
        msgStr = smsMessage.encode('utf-8')
        
        log.info(" << %s" % msgStr)
        
        return msgStr
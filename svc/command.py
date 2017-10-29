'''
Created on 29-10-2017

@author: esanchez
'''

from exception import YaiRoverException
from enumrobot.commons import CommonsEnum
from enumrobot.component import ComponentEnum
from model.vo import YaiCommand, YaiResult
from lib.logger import logger as log
import threading
from svc.communicator.i2c import I2CSvc
from svc.communicator.serial import YaiSerialSvc
import time

class YaiCommandSvc():

    i2cSvc = I2CSvc()
    yaiSerialSvc = YaiSerialSvc()

    def buildMessage(self, yaiCommand = None):
    
        if yaiCommand is None:
            raise YaiRoverException("yaiCommand no puede ser nulo")
    
        if yaiCommand.type is None:
            raise YaiRoverException("yaiCommand.type no puede ser nulo")
    
        yaiCommand.message = "%s,%s,%s,%s,%s,%s,%s,%s,%s" %(yaiCommand.TIPO_CALL, yaiCommand.COMMAND, 
                                                      yaiCommand.P1, yaiCommand.P2, yaiCommand.P3, yaiCommand.P4, 
                                                      yaiCommand.P5, yaiCommand.P6, yaiCommand.P7)        
        yaiCommand.execute = False
        
        if((yaiCommand.type == CommonsEnum.YAI_COMMAND_TYPE_SERIAL.value) 
            or (yaiCommand.type == CommonsEnum.YAI_COMMAND_TYPE_I2C.value)):
            yaiCommand.execute = True                        
        return yaiCommand    
    
    def executeAsync(self, yaiCommand = None, asyncArg = False):
        yaiResult = YaiResult()
        if(asyncArg):
            log.debug("Execute Async")
            yaiResult.status = CommonsEnum.STATUS_OK.value;
            yaiResult.type = CommonsEnum.YAI_COMMAND_TYPE_RESULT.value
            yaiResult.content = "{\"async\": %s}" % asyncArg
            threadCmd = threading.Thread(target=self.execute, args = {yaiCommand: yaiCommand}, name='CmdExecute')
            threadCmd.start()
        else:
            yaiResult = self.execute(yaiCommand)        
        return yaiResult
    
    def execute(self, yaiCommand = None):
        
        if yaiCommand is None:
            raise YaiRoverException("yaiCommand no puede ser nulo")
    
        if yaiCommand.execute is None:
            raise YaiRoverException("yaiCommand.execute no puede ser nulo")      
        
        log.info("Execute Command")
        propagate = False;
        content = "Command not found";
        resultStr = CommonsEnum.STATUS_NOK.value;
        responseCommand = None
        
        yaiResult = YaiResult()
         
        if(yaiCommand.execute):
            #self.yaiCommunicator.sendCommand("I2C,100001,1001,0,0,10002,None,None,None", I2c.CLIENT_ADDR_YAI_MOTOR)            
            command = yaiCommand.COMMAND
            component = yaiCommand.COMPONENT
            
            log.info("cmd::" + command)
            
            if command is None:
                raise YaiRoverException("yaiCommand.COMMAND no puede ser nulo")                                    

            componentEnum = ComponentEnum[component]
            log.info(componentEnum)
            #Comandos que se propagan con delay
            #if ((component == ComponentEnum.RIGHT_HAND.name)):
            resultStr = CommonsEnum.STATUS_OK.value
            propagate = True
            if (not yaiCommand.P5 is None) and (yaiCommand.P5.isnumeric()):
                tiempoStop = int(yaiCommand.P5)
                time.sleep(tiempoStop)

            yaiCommand.address = componentEnum.value                
            log.debug("antes de propagar YaiMotor")
            yaiResult = self.propagateCommand(yaiCommand)
            log.debug("despues de propagar YaiMotor")                                                          
                
        if propagate :
            content = "{\"propagate\": \"%s\"}" % yaiCommand.type
        
        yaiResult.content = content
        yaiResult.status = resultStr
        yaiResult.propagate = propagate
        return yaiResult

    
    def propagateCommand(self, yaiCommand):
        response = None
        yaiResult = YaiResult()
        yaiResult.status = CommonsEnum.STATUS_NOK.value
        if (yaiCommand.type == CommonsEnum.YAI_COMMAND_TYPE_SERIAL.value):
            log.debug("SERIAL >> Propagate");
            yaiResult.status = CommonsEnum.STATUS_OK.value
            yaiResult.message = yaiCommand.message
            yaiResult.type = CommonsEnum.YAI_COMMAND_TYPE_RESULT.value
            responseCommand = self.yaiSerialSvc.sendCommand(yaiCommand.message, yaiCommand.serialPort)
            yaiResult.__resToObject__(responseCommand)
        
        if (yaiCommand.type == CommonsEnum.YAI_COMMAND_TYPE_I2C.value):
            log.debug("I2C >> Propagate");
            yaiResult.status = CommonsEnum.STATUS_OK.value
            responseCommand = self.i2cSvc.sendCommand(yaiCommand.message, yaiCommand.address)
            yaiResult.__resToObject__(responseCommand)
                    
        return yaiResult
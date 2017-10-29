'''
Created on 22-08-2017

@author: instala
'''
from model import AbstractUtilDTO
#from enumrobot import EnumCommons, EnumCommunicator
from enumrobot.commons import CommonsEnum
from enumrobot.serial import SerialEnum
from lib.logger import logger as log

class YaiNetwork(AbstractUtilDTO):
    broadcast = None
    netmask = None
    addr = None
    mac = None

class YaiCommand(AbstractUtilDTO):
    execute = False
    printCmd = False
    propagate = False
    message = ""    
    type = CommonsEnum.YAI_COMMAND_TYPE_NONE.value    
    TIPO_CALL = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    COMMAND = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    P1 = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    P2 = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    P3 = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    P4 = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    P5 = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    P6 = CommonsEnum.YAI_COMMAND_TYPE_NONE.value    
    P7 = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    COMPONENT = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    address = 0x00
    json = ""
    serialPort = SerialEnum.SERIAL_TTYS1_PORT.value

    def __resToObject__(self, msgList = None):
        msg = msgList[0]
        self.message = msg
        resMsgArray = msg.split(",")
        self.type = resMsgArray[0]        
        self.COMMAND = resMsgArray[1]
        self.P1 = resMsgArray[2]
        self.P2 = resMsgArray[3]
        self.P3 = resMsgArray[4]
        self.P4 = resMsgArray[5]
        self.P5 = resMsgArray[6]
        self.P6 = resMsgArray[7]
        self.P7 = resMsgArray[8]
    
    
class YaiResult(AbstractUtilDTO):
    status = None
    content = ""
    message = ""
    R1 = None
    R2 = None
    R3 = None
    R4 = None
    type = CommonsEnum.YAI_COMMAND_TYPE_NONE.value
    
    def __resToObject__(self, msg = None):
        msg = msg.replace("#", "")
        resMsgArray = msg.split(",")
        self.message = msg
        self.type = resMsgArray[0]
        countR = 0     
        for r in resMsgArray:
            if countR > 0:
                setattr(self, "R%d"%countR, r)
            countR = countR + 1        
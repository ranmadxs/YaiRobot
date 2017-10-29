'''
Created on 21-08-2017

@author: instala
'''

from enum import Enum

class CommonsEnum(Enum):
    YAI_COMMAND_TYPE_SERIAL             =       "SERIAL"
    YAI_COMMAND_TYPE_SPI                =       "SPI"
    YAI_COMMAND_TYPE_WIFI               =       "WIFI"
    YAI_COMMAND_TYPE_RESULT             =       "RESULT"
    YAI_COMMAND_TYPE_NONE               =       "NONE"
    YAI_COMMAND_TYPE_I2C                =       "I2C"
    STATUS_OK                           =       "OK"
    STATUS_NOK                          =       "NOK"
    YAI_LOG_FOLDER                      =       "/logs"
'''
Created on 28-10-2017

@author: esanchez
'''

from django.shortcuts import render
from lib.logger import logger as log
from model.vo import YaiCommand, YaiResult
import ast
from django.http import HttpResponse
from svc.command import YaiCommandSvc

class CommandController():
    
    yaiCommandSvc = YaiCommandSvc()
    
    def exe(self, request, asyncArg='False'):
        log.info("CmdController exe")   
        yaiResponse = YaiResult()    
        yaiCommand = YaiCommand(request)
        yaiCommand.type = yaiCommand.TIPO_CALL
        yaiCommand = self.yaiCommandSvc.buildMessage(yaiCommand)        
        log.debug(yaiCommand.__str__())
        exeAsync = ast.literal_eval(asyncArg.capitalize());
        yaiResponse = self.yaiCommandSvc.executeAsync(yaiCommand, exeAsync)
            
        #en el return debe estar el string que devuelve el servicio    
        return HttpResponse(yaiResponse.__str__())                      
        
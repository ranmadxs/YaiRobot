from django.core.handlers.wsgi import WSGIRequest
from django.utils.datastructures import MultiValueDictKeyError
from lib.logger import logger as log
from _ast import IsNot

class AbstractUtilDTO:
    def __init__(self, dictionary = None):
        parseObj = False
                                
        if type(dictionary) is WSGIRequest:
            log.info("WSGIRequest")
            for name in dir(self):
                if not name.startswith('__') :
                    valReq = None
                    try:
                        valReq = dictionary.GET[name]
                    except MultiValueDictKeyError: 
                        pass
                    if not valReq is None:
                        setattr(self, name, valReq)
            parseObj = True
        
        if dictionary != None and not parseObj:
            for k, v in dictionary.items():
                setattr(self, k, v)
                            
    def __str__(self):
        var = dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))     
        varStr = var.__str__().replace("'", '"')
        return '{"%s" : %s}' % (self.__class__, varStr)  
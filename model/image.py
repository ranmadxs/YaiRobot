'''
Created on 04-11-2017

@author: esanchez
'''
from model import AbstractUtilDTO

class YaiRect(AbstractUtilDTO):
    m = None
    b = None
    
    def __init__(self):
        self.m = None
        self.b = None

class YaiPoint(AbstractUtilDTO):
    x = None
    y = None    
    
    def __init__(self):
        self.x = None
        self.y = None
    
    def getPoint(self):
        return (self.x, self.y)
    
    
class YaiFinger(AbstractUtilDTO):
    name = None
    rects = []
    point = None
    pendiente = None
    
    def __init__(self):
        self.name = None
        self.rects = []
        self.point = None
        self.pendiente = None

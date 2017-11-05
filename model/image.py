'''
Created on 04-11-2017

@author: esanchez
'''
from model import AbstractUtilDTO

class YaiPoint(AbstractUtilDTO):
    x = None
    y = None
    point = ()
    
class YaiFinger(AbstractUtilDTO):
    name = None
    points = []
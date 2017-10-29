'''
Created on 13-08-2017

@author: esanchez
'''

import logging

#logging.basicConfig()
logger = logging.getLogger("YaiRobot")
logger.setLevel(logging.DEBUG)


# create console handler and set level to debug
logHandler = logging.StreamHandler()
logHandler.setLevel(logging.DEBUG)

# create formatter
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] <%(pathname)s> L%(lineno)s %(message)s",
                              "%Y-%m-%d %H:%M:%S")
# add formatter to ch
logHandler.setFormatter(logFormatter)

# add handler to logger
logger.addHandler(logHandler)
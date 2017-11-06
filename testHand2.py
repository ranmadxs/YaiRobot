'''
Created on 04-11-2017

@author: esanchez
'''

import cv2
import numpy as np
from svc.image.hand import HandReconigtionSvc
from model.image import YaiPoint
from pygame.time import delay


#Open Camera object
cap = cv2.VideoCapture(0)
skin_min = np.array([0, 40, 150], np.uint8)
skin_max = np.array([20, 150, 255], np.uint8)

#skin_min = np.array([0, 60, 140], np.uint8)
#Decrease frame size
cap.set(3,640)
cap.set(4,480)
font = cv2.FONT_HERSHEY_SIMPLEX

while(1):
        #Capture frames from the camera
    handReconigtionSvc = HandReconigtionSvc()
    #delay(2000)
    
    ret, frame = cap.read()
    
    gaussian_blur = cv2.GaussianBlur(frame, (5, 5), 0)
    blur_hsv = cv2.cvtColor(gaussian_blur, cv2.COLOR_BGR2HSV)

    tre_green = cv2.inRange(blur_hsv, skin_min, skin_max)
    __, contours, hierarchy = cv2.findContours(tre_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    handReconigtionSvc.setImage(frame)
    yaiCenterP = handReconigtionSvc.getCenter(contours)
    #if (yaiCenterP is not None):
        #cv2.putText(frame,'*',tuple(yaiCenterP.point),font,1,(0,0,255),1)


    #if (handReconigtionSvc.totalContours > 20):
        ##### Show final image ########
    cv2.imshow('Result',frame)

    del handReconigtionSvc
    #close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
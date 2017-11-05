'''
Created on 04-11-2017

@author: esanchez
'''
import cv2
import numpy as np
import copy
import math

#handReconigtionSvc = HandReconigtionSvc()

imageName = "resources/imgs/hand/hand5F.jpg"
image = cv2.imread(imageName)
font = cv2.FONT_HERSHEY_SIMPLEX

imageBackGround = "resources/imgs/hand/handBg.jpg"

imageBg = cv2.imread(imageBackGround)

imgEnd = cv2.subtract(image,imageBg)

cv2.imshow(imageName,imgEnd)
cv2.waitKey(0)
cv2.destroyAllWindows()
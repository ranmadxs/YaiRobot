'''
Created on 13-11-2017

@author: instala
'''
import cv2
import numpy as np
from model.image import YaiPoint

font = cv2.FONT_HERSHEY_SIMPLEX
img = cv2.imread('resources/imgs/tre_green.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)





cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
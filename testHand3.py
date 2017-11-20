'''
Created on 04-11-2017

@author: esanchez
'''
import cv2
import numpy as np
import copy
import math
from model.image import YaiPoint

#handReconigtionSvc = HandReconigtionSvc()

imageName = "resources/imgs/tre_greenv3.jpg"
image = cv2.imread(imageName)
font = cv2.FONT_HERSHEY_SIMPLEX
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(grey, (35,35), 0)
thresh1 = cv2.threshold(blurred, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
__, contours, hierarchy = cv2.findContours(grey,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
#__, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#__, contours, hierarchy = cv2.findContours(image.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                          #cv2.findContours(tre_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#cnt = np.concatenate((np.array(contours[0]), np.array(contours[1])), axis=0)
cnt = np.array(contours[0]) 
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
c = np.concatenate((a, b), axis=0)
#cnt = np.concatenate(cnt, contours[1])
print len(contours)
count = 0
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
'''
for contour in contours:
    for cpoint in contour:
        x = cpoint[0][0]
        y = cpoint[0][1]
        cv2.putText(image,'.',tuple((x, y)),font,.5,(255,0,0),1)

hull = cv2.convexHull(cnt)

M = cv2.moments(cnt[0])
print M
'''
cv2.imshow(imageName,image)
cv2.waitKey(0)
cv2.destroyAllWindows()
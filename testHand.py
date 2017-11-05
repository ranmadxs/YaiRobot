'''
Created on 04-11-2017

@author: esanchez
'''
import cv2
import numpy as np
from svc.image.hand import HandReconigtionSvc
from model.image import YaiPoint


handReconigtionSvc = HandReconigtionSvc()

imageName = "resources/imgs/hand0F.jpg"
image = cv2.imread(imageName)
font = cv2.FONT_HERSHEY_SIMPLEX

skin_min = np.array([0, 40, 150], np.uint8)
skin_max = np.array([20, 150, 255], np.uint8)
#131, 92, 95
skin_min = np.array([0, 60, 140], np.uint8)



gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
blur_hsv = cv2.cvtColor(gaussian_blur, cv2.COLOR_BGR2HSV)

tre_green = cv2.inRange(blur_hsv, skin_min, skin_max)
__, contours, hierarchy = cv2.findContours(tre_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


handReconigtionSvc.setImage(image)
yaiCenterP = handReconigtionSvc.getCenter(contours)

print yaiCenterP

cv2.imshow(imageName,image)
cv2.waitKey(0)
cv2.destroyAllWindows()
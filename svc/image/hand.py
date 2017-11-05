'''
Created on 04-11-2017

@author: esanchez
'''
import cv2
import numpy as np
from lib.logger import logger as log
from model.image import YaiPoint
import math

class HandReconigtionSvc():
    
    totalContours = 0
    maxContour = []
    font = cv2.FONT_HERSHEY_SIMPLEX    
    image = None
    
    def setImage(self, imageIn):
        self.image = imageIn
    
    def calcPromedio(self, contours):
        mx = 0
        my = 0
        for contour in contours:
            mx = mx + contour[0]
            my = my + contour[1]
        
        mx = mx / len(contours)
        my = my / len(contours)
        
        mPoint = YaiPoint()
        mPoint.x = mx
        mPoint.y = my
        mPoint.point = (mx, my)
        return mPoint
    
    def findMinPoint(self, contours, descEst):
        minX = None
        minY = None
        point = YaiPoint()
        for contour in contours:
            if minX == None or minX > contour[0] :
                minX = contour[0]
                minY = contour[1]

        for contour in contours:
            if minY > contour[1] and math.fabs(contour[0] - minX) < descEst.x/8:
                minX = contour[0]
                minY = contour[1]

        point.x = minX
        point.y = minY
        point.point = (minX, minY)        
        print "pmin%s"%point        
        subConjuntoAux = []
        cv2.putText(self.image,'o',tuple(point.point),self.font,1,(255,0,0),2)
        
        for contour in contours:
            if contour[0] > minX + (descEst.x /8):
                subConjuntoAux.append(contour)

        if len(subConjuntoAux) > 0:
            self.findMinPoint(subConjuntoAux, descEst)        
    
    def calcDesvEst(self, contours):
        
        mPoint = self.calcPromedio(contours)
        desvEstx = 0
        desvEsty = 0        
        
        for contour in contours:
            desvEstx = desvEstx + math.pow(contour[0] - mPoint.x, 2)
            desvEsty = desvEsty + math.pow(contour[1] - mPoint.y, 2)
            
        desvEstx = desvEstx / len(self.maxContour)
        desvEsty = desvEsty / len(self.maxContour)
            
        desvEstx = math.sqrt(desvEstx)
        desvEsty = math.sqrt(desvEsty)        

        desPoint = YaiPoint()
        desPoint.x = desvEstx
        desPoint.y = desvEsty
        desPoint.point = (desvEstx, desvEsty)
        return desPoint
    
    def getCenter(self, contours):
        self.totalContours = len(contours)
        log.info(self.totalContours)
        if len(contours) > 0 :
            sx = 0
            sy = 0
            totalAll = 0
            ax = 0
            ay = 0

            for contour in contours:
                #log.debug("===== %d ========="%self.totalContours)
                spx = 0
                spy = 0
                totalPContour = 0
                maxXC = 0
                maxYC = 0                
                for cpoint in contour:
                    totalPContour = totalPContour + 1
                    xc = cpoint[0][0]
                    yc = cpoint[0][1]
                    if (yc >maxYC) :
                        maxYC = yc
                        maxXC = xc
                    point = (xc, yc)
                    #log.debug(point)
                    #cv2.putText(self.image,'.',point,self.font,1,(255,255,255),1)
                    spx = spx + xc
                    spy = spy + yc

                self.maxContour.append((maxXC, maxYC))
                #cv2.putText(self.image,'.',(maxXC, maxYC),self.font,1,(255,255,255),1)                    
                sx = sx + (spx / totalPContour)
                sy = sy + (spy / totalPContour)
                ax = ax + spx
                ay = ay + spy
                totalAll = totalPContour + totalAll
            
            mx = sx / self.totalContours
            my = sy / self.totalContours

            amx = ax / totalAll
            amy = ay / totalAll

            log.info("Total Contour: %d" %self.totalContours)
            centerMass=((mx + amx)/2, (my + amy)/2)
            centerPoint = YaiPoint()
            centerPoint.x = centerMass[0]
            centerPoint.y = centerMass[1]
            centerPoint.point = centerMass          
            
            subConjuntoDedos = []
            for contour in self.maxContour:
                if (contour[1] < centerPoint.y ) :
                    #and contour[0] < centerPoint.x
                    subConjuntoDedos.append(contour) 
                        
            subConjuntoDedos = self.maxContour
            desvEst = self.calcDesvEst(subConjuntoDedos)
            
            print " ===== DESV EST ====== "
            print desvEst
            print " ===== ======= ====== "
            
            self.findMinPoint(subConjuntoDedos, desvEst)
            
            for contour in subConjuntoDedos:
                #and contour[0] > centerPoint.x
                #or (contour[0] > centerPoint.x):
                cv2.putText(self.image,'%d.%d'%(contour[0], contour[1]),(contour[0], contour[1]),self.font,0.3,(0,0,0),1)
            #    cv2.putText(self.image,'.',(contour[0], contour[1]),self.font,0.8,(0,255,0),1)
                #print (contour[0], contour[1])

            cv2.putText(self.image,'%d*%d'%(centerPoint.x, centerPoint.y),tuple(centerPoint.point),self.font,1,(0,0,255),1)
            return centerPoint
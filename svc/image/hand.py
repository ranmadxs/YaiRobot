'''
Created on 04-11-2017

@author: esanchez
'''
import cv2
import numpy as np
from lib.logger import logger as log
from model.image import YaiPoint, YaiRect
import math
from dis import distb

#TODO: Eliminar puntos que se encuentran muy alejados del centro de masa (2desvest)
class HandReconigtionSvc():
    
    def __init__(self):    
        self.maxpend = 0.5       
        self.totalContours = 0
        self.maxContour = []
        self.minPoints = []
        self.font = cv2.FONT_HERSHEY_SIMPLEX    
        self.image = None
        self.centerPoint = YaiPoint()
        self.baseHand = YaiPoint()
    
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
            if minY > contour[1] and math.fabs(contour[0] - minX) < descEst.x/16:
                minX = contour[0]
                minY = contour[1]

        point.x = minX
        point.y = minY
        point.point = (minX, minY)        
        #print "pmin%s"%point        
        return point
    
    def finMinPendientPointOld(self, contours, descEst):
        mpoint = self.findMinPoint(contours, descEst)        
        dy = (mpoint.y - self.baseHand.y)
        dx = (mpoint.x - self.baseHand.x)
        mpen = float(dy) / float(dx)
        
        subConjuntoAux = []
        
        log.info ("mpen %s %s/%s=%s" %(mpoint.getPoint(), mpen, dy, dx))
              
        for contour in contours:            
            if float(contour[0] - self.baseHand.x) != 0:                
                cpen = float(contour[1] - self.baseHand.y) / float(contour[0] - self.baseHand.x)
                log.debug("rr> %s  %s"%(contour, cpen))
                #ESTE IF DEBO PENSARLO SUPER BIEN AHORA ESTA PESIMO Y FUNCIONA DE CASUALIDAD, ALGORITMO CORRECTO DEBE SER: TIRAR REXCTAS PARALELAS Y VER PUNTOS ENTRE ELLAS
                # Y DEBO PONER SOLO LOS PUNTOS DE DEDOS HACIA ARRIBA Y LUEGO VEO EL DEDO GORDO
                if not(cpen <= mpen + self.maxpend and cpen >= mpen - self.maxpend) and (contour[0] > mpoint.x + descEst.x/2):
                    
                    subConjuntoAux.append(contour)
                    log.info( "%s -> %s" % (contour, cpen))
                else:                    
                    if contour[1] < mpoint.y :                    
                        mpoint.x = contour[0]
                        mpoint.y = contour[1]
                        log.info( ">>> Arreglando mpoint %s, %s   %s" %(mpoint.x, mpoint.y, cpen))
                    else:
                        log.info( "Se descarta %s   %s <por> %s, %s    %s" %(contour, cpen, mpoint.x, mpoint.y, mpen))
            else :
                log.info ("WTFFFF %s"%contour)
                     
        cv2.putText(self.image,'.',tuple(mpoint.getPoint()),self.font,1.5,(0,255,0),2)
        cv2.circle(self.image,mpoint.getPoint(), int(descEst.x/4), (0,255,0), 1)

        log.info ("=============== %s %s" %(mpoint.getPoint(), mpen))

        countEl = 0
        if len(subConjuntoAux) > 0:
            for contour in subConjuntoAux:
                distBtw = self.calcDistPoints(mpoint.getPoint(), (contour[0], contour[1]))
                if (distBtw <= int(descEst.x/4)):
                    print "Removiendo punto %s (%s <= %s)"%(contour, distBtw, int(descEst.x/4))
                    subConjuntoAux.remove(contour)
            if len(subConjuntoAux) > 0:                    
                self.finMinPendientPoint(subConjuntoAux, descEst)

    def calcRect(self, point, descEst):
        arrayRect = []
        bpx = float((point.x + self.centerPoint.x) /2)
        bpy = self.centerPoint.y
        dy = (bpy - point.y)
        dx = (bpx - point.x)
        m = float(dy) / float(dx)
        rect = YaiRect()
        rect.m = m
        rect.b = float(bpy) - float(m*bpx)
        cv2.line(self.image, point.getPoint(), (int(bpx), int(bpy)), (0, 0, 255), 1, 8)
        arrayRect.append(rect)
        
        
        dx = descEst.x/4
        
        rect2 = YaiRect()
        r2x = point.x + dx
        r2y = point.y
        rect2.m = m
        rect2.b = float(r2y) - float(m*r2x)                            
        cv2.line(self.image, (int(r2x), int(r2y)), (int(bpx + dx), int(bpy)), (0, 0, 255), 1, 8)
        arrayRect.append(rect2)
        
        rect3 = YaiRect()        
        r3x = point.x - dx
        r3y = point.y
        rect3.m = m
        rect3.b = float(r3y) - float(m*r3x)
        arrayRect.append(rect3)

        cv2.line(self.image, (int(r3x), int(r3y)), (int(bpx - dx), int(bpy)), (0, 0, 255), 1, 8)                
        
        return arrayRect
    
    def distPoint2Rect(self, point, arrayRect, descEst):
        dist = 9999
        for rect in arrayRect:
            #log.info(rect)
            distAux = math.fabs((rect.m * point.x) - point.y + rect.b)/float(math.sqrt(rect.m*rect.m + 1))
            #log.info(distAux) 
            if dist > distAux:                
                dist = distAux 
        return dist

    def finMinPendientPoint(self, contours, descEst):
        mpoint = self.findMinPoint(contours, descEst)        
        dy = (mpoint.y - self.baseHand.y)
        dx = (mpoint.x - self.baseHand.x)
        mpen = float(dy) / float(dx)
        
        subConjuntoAux = []
        
        log.info ("mpen %s %s/%s=%s" %(mpoint.getPoint(), dy, dx, mpen))
        arrayRect = self.calcRect(mpoint, descEst)
              
        arrayPendientes = []
        arrayDedo = []
        for contour in contours:   
            
            if contour[0] != mpoint.x and contour[1] != mpoint.y:                        
                point = YaiPoint()
                point.x = contour[0]
                point.y = contour[1]   
                distMin = self.distPoint2Rect(point, arrayRect, descEst)
                #log.debug(distMin) 
                if (distMin <= descEst.x / 2):
                    #cv2.putText(self.image,'O',tuple(point.getPoint()),self.font,1.5,(255,0,255),2)
                    log.debug("(--) %s %s"%(point.getPoint(), ""))                    
                    arrayDedo.append(contour)
                else:
                    log.debug("(++) %s %s"%(point.getPoint(), ""))
                    arrayPendientes.append(contour)

        if len(arrayDedo) > 1:
            for contour in arrayDedo:
                if contour[1] < mpoint.y :
                    log.info( ">>> Arreglando %s por %s " %(mpoint.getPoint(), contour))                    
                    mpoint.x = contour[0]
                    mpoint.y = contour[1]                    
                     
        cv2.putText(self.image,'.',tuple(mpoint.getPoint()),self.font,1.5,(0,255,0),2)
        cv2.circle(self.image,mpoint.getPoint(), int(descEst.x/2), (0,255,0), 1)

        log.info ("=============== %s %s" %(mpoint.getPoint(), mpen))
        
        if len(arrayPendientes) >= 1:
            self.finMinPendientPoint(arrayPendientes, descEst)
        
    
    def calcDistPoints(self, p1, p2):
        dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        return dist
        
    def findMinPoints(self, contours, descEst):
        point = self.findMinPoint(contours, descEst)
        cv2.putText(self.image,'%d, %d'%(point.x, point.y),tuple(point.point),self.font,.5,(255,0,0),1)
      
        #print "pmin%s"%point        
        subConjuntoAux = []
        #cv2.putText(self.image,'%do%d'%(minX, minY),tuple(point.point),self.font,.5,(255,0,0),1)
        self.minPoints.append(point.getPoint())
                
        for contour in contours:
            if contour[0] > point.x + (descEst.x /16):
                subConjuntoAux.append(contour)

        if len(subConjuntoAux) > 0:
            self.findMinPoints(subConjuntoAux, descEst)        
    
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
        height, width, channels = self.image.shape
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
                    #point = (xc, yc)
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
            self.centerPoint.x = centerMass[0]
            self.centerPoint.y = centerMass[1]     
                                               
            #subConjuntoDedos = self.maxContour
            desvEst = self.calcDesvEst(self.maxContour)
            
            self.baseHand.x = self.centerPoint.x
            self.baseHand.y = height - 2*int(desvEst.y)             

            log.info("Base Hand (%s, %s)"%(self.baseHand.x, self.baseHand.y))

            mainRadio = int(math.fabs(self.centerPoint.y - self.baseHand.y))
            
            log.info( "centerPoint: %s"%self.centerPoint)
            
            log.info(" ===== DESV EST ====== ")
            log.info( desvEst)
            log.info(" ===== ======= ====== ")
            
            subConjuntoDedos = [] 
            for contour in self.maxContour:
                if (self.centerPoint.y  > contour[1] ):
                    #+ desvEst.y
                    #cv2.putText(self.image,'%d.%d'%(contour[0], contour[1]),(contour[0], contour[1]),self.font,0.3,(0,0,0),1)       
                    subConjuntoDedos.append(contour)
            
            self.findMinPoints(subConjuntoDedos, desvEst)
            
            subConjuntoMax = []
            log.info("=== MIN POINTS ===")
            for contour in self.minPoints:                
                disp = self.calcDistPoints(self.centerPoint.getPoint(), (contour[0], contour[1]))
                if (disp > mainRadio) :
                    log.debug(contour)
                #if (self.centerPoint.y > contour[1] ) and (disp > mainRadio):
                    subConjuntoMax.append(contour)
            
            if len(self.minPoints) > 0:
                self.finMinPendientPoint(subConjuntoMax, desvEst)
            
            #pointMin = self.findMinPoint(subConjuntoDedos, desvEst)
            #print pointMin
            #cv2.putText(self.image,'(%d,%d)'%(pointMin.x, pointMin.y),tuple(pointMin.getPoint()),self.font,.5,(255,0,0),1)
            
            for contour in subConjuntoDedos:
                cv2.putText(self.image,'%d.%d'%(contour[0], contour[1]),(contour[0], contour[1]),self.font,0.3,(0,0,0),1)

            cv2.putText(self.image,'%d*%d'%(self.centerPoint.x, self.centerPoint.y),tuple(self.centerPoint.getPoint()),self.font,1,(0,0,255),1)
                       
            
            cv2.line(self.image, self.baseHand.getPoint(), self.centerPoint.getPoint(), (0, 0, 255), 1, 8)
            
            cv2.circle(self.image,self.centerPoint.getPoint(), mainRadio, (0,0,255), 1)
            
            cv2.putText(self.image,'C',tuple(self.baseHand.getPoint()) ,self.font,1,(255,0,0),2)
            return self.centerPoint
import cv2
import numpy

import matplotlib.pyplot as plt


class Detector(object):
    lbpCascade = cv2.CascadeClassifier('cascades/doot.xml')

    #lbpCascade = cv2.CascadeClassifier('cascades/lbp0.xml')
    haarCascade = cv2.CascadeClassifier('cascades/haar.xml')
    
    def lbp(self, img):
        toDetect = img.copy()
        
        toDet = cv2.cvtColor(toDetect, cv2.COLOR_BGR2GRAY)
        hornRect = self.lbpCascade.detectMultiScale(toDet, scaleFactor = 1.1, minNeighbors = 175)
        
        for (x, y, w, h) in hornRect:
            cv2.rectangle(toDet, (x, y), (x+w, y +h), (10, 10, 200), 10)
                          
        return toDet

    def haar(self, img):
        toDetect = img.copy()
        
        hornRect = self.lbpCascade.detectMultiScale(toDetect, scaleFactor = 1.2, minNeighbors = 25)
        
        for (x, y, w, h) in hornRect:
            cv2.rectangle(toDetect, (x, y), (x+w, y+h), (10, 200, 10), 10)
            
        return toDetect

vido = cv2.VideoCapture(0)
det = Detector()


while(True):
    #Get the video frame
    ret, frame = vido.read()
    
    #detect using lbp
    toUseLBP = frame.copy()
    im = det.lbp(toUseLBP)
    
    
    #detect using haar
    #toUseHaar = frame.copy()
    #im = det.haar(toUseHaar)
    
    #Show the image
    cv2.imshow('lbp vs haar', im)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vido.release()
cv2.destroyAllWindows()
    
    

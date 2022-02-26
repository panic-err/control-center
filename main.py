import cv2
import numpy
import os
import matplotlib.pyplot as plt

from pathlib import Path

class Detector(object):
    lbpCascade = cv2.CascadeClassifier('cascades/wakizashi.xml')

    #lbpCascade = cv2.CascadeClassifier('cascades/lbp0.xml')
    haarCascade = cv2.CascadeClassifier('cascades/haar.xml')
    
    def lbp(self, img):
        toDetect = img.copy()
        count = 0
        toDet = cv2.cvtColor(toDetect, cv2.COLOR_BGR2GRAY)
        hornRect = self.lbpCascade.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        
        for (x, y, w, h) in hornRect:
            cv2.rectangle(toDet, (x, y), (x+w, y +h), (10, 10, 200), 10)
            count += 50  
            #print("testing print function")
            #with open() as f:
            #    read_data = f.read()
                
            #if f.closed:
            #    print("file already closed")
            #file = os.open('rw+', str(count)+".txt")
            #file.close()
        if count == 0:
            count = -1
        return toDet, count

    def haar(self, img):
        toDetect = img.copy()
        
        hornRect = self.lbpCascade.detectMultiScale(toDetect, scaleFactor = 1.2, minNeighbors = 25)
        
        for (x, y, w, h) in hornRect:
            cv2.rectangle(toDetect, (x, y), (x+w, y+h), (10, 200, 10), 10)
            
        return toDetect
#import dector
vido = cv2.VideoCapture(0)
det = Detector()
p = Path('.')
[x for x in p.iterdir() if x.is_dir()]
l = list(p.glob('**/*.py'))
print(l)
c = 0
while(True):
    #Get the video frame
    try:
        ret, frame = vido.read()
    except e:
        print(e)
        #e as NoneType
    #detect using lbp
    toUseLBP = frame.copy()
    im, d = det.lbp(toUseLBP)
    if d > 0:
        c += d
    
    #if d == -1:
    #    print("No detection")
    #else:
    #    c += d
    
    #detect using haar
    #toUseHaar = frame.copy()
    #im = det.haar(toUseHaar)
    #print(str(c))
    #Show the image
    cv2.imshow('lbp vs haar', im)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vido.release()
cv2.destroyAllWindows()
    
    

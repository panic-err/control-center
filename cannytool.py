import cv2
import numpy
import os
import matplotlib.pyplot as plt

from pathlib import Path

class Detector(object):
    
    #lbp
    #wakizashi = cv2.CascadeClassifier('cascades/wakizashi.xml')
    #count = 0
    #bastardsword = cv2.CascadeClassifier('cascades/bastardsword.xml')
    #doot = cv2.CascadeClassifier('cascades/doot.xml')
    #fouram = cv2.CascadeClassifier('cascades/fouram.xml')
    #longbl = cv2.CascadeClassifier('cascades/longbl.xml')
    #sword = cv2.CascadeClassifier('cascades/sword.xml')
    #lbpCascade = cv2.CascadeClassifier('cascades/lbp0.xml')
    libpClay = cv2.CascadeClassifier('cascades/gummywurm.xml')
    count = 0
    #haar
    #haarCascade = cv2.CascadeClassifier('cascades/haar.xml')
    
    def lbp(self, img):
        toDetect = img.copy()
        self.count = 0
        toDet = cv2.cvtColor(toDetect, cv2.COLOR_BGR2GRAY)
        t = toDet.copy()
        #hornRect = self.lbpCascade.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #wakizashi0 = self.wakizashi.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #bastardsword0 = self.bastardsword.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #doot0 = self.doot.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #fouram0 = self.fouram.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #longbl0 = self.longbl.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #sword0 = self.sword.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        clay0 = self.libpClay.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 3)
        
        for (x, y, w, h) in clay0:
            #if (x <= 239):
            print("Found {0} hands!".format(len(clay0)))
            #self.count += 5*len(clay0)
            #if self.count >= 5:
            cv2.rectangle(toDet, (x, y), (x+w, y+h), (10, 10, 200), 10)
            #    self.count -= 2
            #    self.count = 0
            #cv2.imwrite(str(self.count)+'img.jpg', t)
            #self.count += 1
            #print("writing out image"+str(self.count))
                
        
        #for (x, y, w, h) in wakizashi0:
        #    count += 5000
        #for (x, y, w, h) in bastardsword0:
        #    count += 5000
        #    count += 5000
        #    count += 5000
        #    count += 20000000
        #    cv2.rectangle(toDet, (x, y), (x+w, y +h), (10, 10, 200), 10)
        #    #print(str(count))
        #for (x, y, w, h) in longbl0:
        #    count += 5000
        #for (x, y, w, h) in sword0:
        #    count += 5000
            
        #self.count = count
        
        
        #for (x, y, w, h) in hornRect:
        #    cv2.rectangle(toDet, (x, y), (x+w, y +h), (10, 10, 200), 10)
        #    count += 50  
            #print("testing print function")
            #with open() as f:
            #    read_data = f.read()
                
            #if f.closed:
            #    print("file already closed")
            #file = os.open('rw+', str(count)+".txt")
            #file.close()
        #if count == 0:
        #    count = -1
        #if self.count >= 22222250000:
        #    #print(str(self.count))
        #    self.count = 0
        #self.count = count
        return toDet

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
#print(l)




while(True):
    #Get the video frame
    try:
        ret, frame = vido.read()
    except e:
        print(e)
        #e as NoneType
    #detect using lbp
    toUseLBP = frame.copy()
    im = det.lbp(toUseLBP)
    #imm, e = det.lbp(toUseLBP)
    
    #if d > 0:
    #    c = True
    #    print(str(c))
    #else:
    #    c = False
    #    print(str(c))
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
#vido.close()    
vido.release()
cv2.destroyAllWindows()
    
    

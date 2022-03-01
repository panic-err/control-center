
import cv2
import numpy
import os
import matplotlib.pyplot as plt

from pathlib import Path


import PySide6

print(PySide6.__version__)

import pika
import sys
import time
import psycopg2

import threading
import random
import sys
import os
from random import *
import datetime

from PySide6.QtQuick import QQuickWindow
from PySide6.QtGui import Qt
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtCore import QUrl, Qt, Slot, Property, QThread
from PySide6.QtWidgets import (QWidget, QProgressBar, QFrame, QGraphicsScene, QDialog, QVBoxLayout, QApplication, QLineEdit, QLabel, QPushButton, QGridLayout, QSlider)
#from __feature__ import snake_case


#for opencv stuff
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


class InputBox(QWidget):

    def calc_red(self):
        red = randint(1, 255)
        if red < 0:
            red = 0
        self.red = str(red)
        return red
    def calc_green(self):
        green = randint(1, 255)
        if green < 0:
            green = 0
        self.green = str(green)
        return green
    def calc_blue(self):
        blue = randint(1, 255)
        if blue < 0:
            blue = 0
        self.blue = str(blue)
        return blue

    


    def __init__(self):
        #t = threading.Thread(Heartbeat.__init__)
        #t.start()

        #self.connection = bep.connection

        QWidget.__init__(self)
        self.hello =  [
                "hallo",
                "hi",
                "hola"
                ]

        self.buttons = []
        self.greeters = []
        self.senders = []
        self.resize(800, 150)
        self.layout = QGridLayout(self)
        self.layout.horizontalSpacing()
        self.layout.verticalSpacing()
        #self.setStyleSheet("QGridLayout {background-image: url('../art/pastel.png') 0 0 0 0 stretch stretch;color:green;}")
        #self.layout = QGridLayout(self)
        for i in range(2):
            self.setWindowTitle("Input Bar")
            mess = QLineEdit("Messages!")
            mess.position = i
            mess.setMaxLength(60)
            mess.returnPressed.connect(self.greet)
            self.greeters.append(mess)
            mess.setStyleSheet("color:aqua;")
            self.layout.addWidget(mess, i, 0)
            #nameButton = QPushButton('PLACEHOLDER')
            nameButton = QSlider()
            #nameButton.clicked.connect(self.name_detail)
            nameButton.setStyleSheet("color:aqua;")
            self.layout.addWidget(nameButton, i, 1)
            button = QPushButton(str(i))
            button.setStyleSheet("color:orange;")
            #self.position = i
            button.position = i
            self.layout.addWidget(button, i, 2)
            send = QPushButton("SEND")
            send.setStyleSheet("color:aqua;")
            send.position = i
            send.clicked.connect(self.greetNoColour)
            button.clicked.connect(self.greet)
            self.senders.append(send)
            self.layout.addWidget(send, i, 3)
            #button.object_name = "butt"+str(i)
            self.buttons.append(button)
            self.setStyleSheet("background-color:#b767bc;")
            self.nameDetail = QDialog()
            self.nameDetailLayout = QVBoxLayout(self.nameDetail)
            nameDetail = "Details"
            labelDetail = QPushButton(nameDetail)
            self.nameDetailLayout.addWidget(labelDetail)

        self.established = False
    @Property(QGraphicsScene)
    @Property(threading.Thread)
    @Property(QWidget)
    def buttonList():
        return self.buttons
    @Property(QWidget)
    def conn():
        return self.connection
    @Slot()
    def name_detail(self):
        #code for showing a string in an array
        if not self.established:
            filename = '101/1.txt'
            out = []
            outString = ""
            count = 0
            with open(filename) as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    outString += lines[i]
                count += 1
            #print(outString)
            l = QLabel(outString)

            self.nameDetail.layout().addWidget(l)
            l.show()
            self.established = True
        #self.nameDetail.setText(outString)
        self.nameDetail.resize(450, 500)
        self.nameDetail.setStyleSheet("background:black;font:Courier New;color:pink;")
        self.nameDetail.show()
    @Slot()
    def greet(self):
        #code for showing a string in an array
        if not self.established:
            filename = '101/1.txt'
            out = []
            outString = ""
            count = 0
            with open(filename) as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    outString += lines[i]
                count += 1
            #print(outString)
            l = QLabel(outString)

            self.nameDetail.layout().addWidget(l)
            l.show()
            self.established = True
        #self.nameDetail.setText(outString)
        self.nameDetail.resize(450, 500)
        self.nameDetail.setStyleSheet("background:black;font:Courier New;color:pink;")
        self.nameDetail.show()        
        
        butt = self.focusWidget()
        
        print("Butt  number"+str(butt.position))
        print(self.greeters[butt.position].text())
        print(butt.position)
    @Slot()
    def greetNoColour(self):
        butt = self.focusWidget()
        #try:
        #    self.emissionNoColour(butt.position)
        #
        #except Exception as e:
        #    print("Probably a closed pipe")
        #    self.reconnect()
        #    #this works!
        #    self.emissionNoColour(butt.position)
        #
        print("Butt  number"+str(butt.position))
        print(self.greeters[butt.position].text())
        print(butt.position)

    @Slot()
    def boop():
        print("boop")
        #self.message.text = random.choice(self.hello)
#class Heartbeat(threading.Thread):
    
class Receiver(InputBox,QThread):
    x, y = 100, 200
    def run(self):

            #widget = RocketWrite()
            #This is because consuming messages is a blocking function
            #recv.drawLines()
            inputb.show()
            #pictureThread = threading.Thread(target=input)
            #pictureThread.start()
            #inputthread = threading.Thread(target=recv.drawLines)
            #t = threading.Thread(target=recv.channel.start_consuming)
            #widget.show()
            #inputthread.start()
            #input.show()
            #t.start()

            #recv.start()
            #recv.drawLines()

            #tt.start()
            #bip = threading.Thread(target=Heartbeat.__init__)
            #bip.start()
            
            print("dootinstart")
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    #vido.close()    
            #    #vido.release()
            #    #cv2.destroyAllWindows()
            #    print("Doot in start")
            #    #break
            #self.appengine.exec()

    def __init__(self, startval=100):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.x = startval
    @Property(int)
    def xVal(self):
        return self.x
    @xVal.setter
    def xVal(self, val):
        self.x = val
    
    @Slot()
    def increaseX(self):
        self.x += 1
        print("Increasing X")
    @Slot()
    def increaseY(self):
        self.y += 1
    @Slot()
    def decreaseX(self):
        self.x -= 1
        print("Decreasing X")
    @Slot()
    def decreaseY(self):
        self.y -= 1
    def updateScreen(self):
        while True:
            self.show()
    def drawLines(self):
        img = cv.imread('stills/horns.jpg',0)
        
        edges = cv.Canny(img, self.x, self.y)
        
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('Original Image'),plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        plt.title('Edge Image' ), plt.xticks([]), plt.yticks([])

        plt.show()
    def consumeCallback(self, ch, method, properties, body):
        print("[x], %r:%r" % (method.routing_key, body))
        bodyStr = str(body)
        print("In loop?")
        if "bip" in bodyStr:
            return
        deconBody = bodyStr.split(":")
        if len(deconBody) < 6:
            bodyStr = "PACKAGE::::"+"::"
            deconBody = bodyStr.split(":")
        if len(deconBody) > 6:
            print("Illegal character found")
            subBody = ""
            for i in range(len(deconBody)):
                if i >= 5:
                    subBody += deconBody[i]
            deconBody[5] = subBody
        if "DRILL" in deconBody[5] and len(deconBody) < 6:
            if self.spacers[int(deconBody[4])-1].coord <= 10:
                self.spacers[int(deconBody[4])-1].coord -= 1
                self.spacers[int(deconBody[4])-1].setValue(self.spacers[int(deconBody[4])-1].coord)
            elif self.spacers[int(deconBody[4])-1].coord > 10:
                self.spacers[int(deconBody[4])-1].coord = 10
            return
        if "SURFACE" in deconBody[5] and len(deconBody) < 6:
            if self.spacers[int(deconBody[4])-1].coord >= 0:
                self.spacers[int(deconBody[4])-1].coord += 1
                self.spacers[int(deconBody[4])-1].setValue(self.spacers[int(deconBody[4])-1].coord)
            elif self.spacers[int(deconBody[4])-1].coord < 0:
                self.spacers[int(deconBody[4])-1].coord = 0
            return
        print(deconBody[0][2:])
        mess = deconBody[5][:-1]
        if deconBody[0][2:] == "PACKAGE":
            print("PACKAGE GET")
            print(deconBody[4])
            #print(deconBody)
            self.greeters[int(deconBody[4])-1].setText(mess)
        if "EXIT" in bodyStr:
            print("bye!")
            self.connection.close()
            sys.exit()
    @Slot()
    def dig(self):
        self.y += 1
        butt = self.focusWidget()
        if self.spacers[butt.position].coord <= 10:
            self.spacers[butt.position].coord -= 1
            self.spacers[butt.position].setValue(self.spacers[butt.position].coord)
        elif self.spacers[butt.position].coord > 10:
            self.spacers[butt.position].coord = 10
    @Slot()
    def surface(self):
        self.x += 1
        butt = self.focusWidget()
        if self.spacers[butt.position].coord >= 0:
            self.spacers[butt.position].coord += 1
            self.spacers[butt.position].setValue(self.spacers[butt.position].coord)
        elif self.spacers[butt.position].coord < 0:
            self.spacers[butt.position].coord = 0


 
    def __init__(self):
        #t = threading.Thread(Heartbeat.__init__)
        #t.start()
        #self.connection = bep.connection
        #bep = Heartbeat()
        #t = threading.Thread(bep.run)
        #t.start()
        #bep.start()
    
        self.position = 0


        QWidget.__init__(self)
        self.hello =  [
                "hallo",
                "hi",
                "hola"
                ]

        self.buttons = []
        self.greeters = []
        self.senders = []
        self.spacers = []
        self.diggers = []
        self.surfacers = []
        self.resize(1115, 550)
        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        #self.setStyleSheet("QGridLayout {background-image: url('../art/pastel.png') 0 0 0 0 stretch stretch;color:green;}")
        #self.layout = QGridLayout(self)
        for i in range(28):
            self.setWindowTitle("Main")
            if i >= 6:
                mess = QLineEdit("Messages!")
                mess.position = i
                mess.coord = 8
            else:
                mess = QLabel("HEADER")
                mess.position = i
                mess.coord = 8
                mess.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
                mess.setText("HEADER")
                mess.setStyleSheet("margin:0 auto;")
                mess.show()
            #mess.returnPressed.connect(self.greet)
            self.greeters.append(mess)
            mess.setStyleSheet("color:aqua;")
            self.layout.addWidget(mess, i, 0, 2, 1)
            if mess.coord < 10:
                spacer = QProgressBar()
                spacer.coord = 8
                spacer.setMaximum(10)
                spacer.setFormat("")
                if i < 10:
                    spacer.setStyleSheet("background-color:#bc6797;")
                    self.layout.addWidget(spacer, i, 6)

                    self.spacers.append(spacer)
            if i < 10:
                nameButton = QPushButton("+")
                nameButton.position = i
                nameButton.clicked.connect(self.increaseX)
                nameButton.clicked.connect(self.surface)
            else:
                nameButton = QPushButton("NAME")
            #nameButton.clicked.connect(self.name_detail)
            nameButton.setStyleSheet("color:aqua;")
            self.layout.addWidget(nameButton, i, 4)
            if i < 10:
                button = QPushButton("-")
                button.position = i
                button.clicked.connect(self.dig)
            elif i <= 20:
                button = QPushButton("addtoX")
                button.clicked.connect(self.increaseX)
            elif i <= 24:
                button = QPushButton("decreaseX")
                button.clicked.connect(self.decreaseX)
            elif i <= 25:
                button = QPushButton("increaseX")
                button.clicked.connect(self.increaseX)
            else:
                button = QPushButton(str(i))
            if i == 10:
                b = QPushButton("Messages as they are added\n0:0:0:0:0:0:0:0:0:0")
                #this should be added to a collection
                self.layout.addWidget(b, i, 6, 28, 1)
            button.setStyleSheet("color:red;")
            #self.position = i
            button.position = i
            self.layout.addWidget(button, i, 5)
            if i < 6:
                head = QPushButton("GLOBAL")
                head.setStyleSheet("background-color:orange;")
                head.position = i
                self.senders.append(head)
                self.layout.addWidget(head, i, 3)
            else:
                #print("And a small green alien that only homer can see")
                send = QPushButton("SEND")
                send.setStyleSheet("color:aqua;")
                send.position = i
                #send.clicked.connect(
                #send.clicked.connect(self.greetNoColour)
                #button.clicked.connect(self.greet)
                self.senders.append(send)
                #self.layout.addWidget(send, i, 3)
            #button.object_name = "butt"+str(i)
            self.buttons.append(button)
            self.setStyleSheet("background-color:#bc6797;")
            self.nameDetail = QDialog()
            self.nameDetailLayout = QVBoxLayout(self.nameDetail)
            nameDetail = "Details"
            labelDetail = QPushButton(nameDetail)
            #labelDetail.clicked.connect(self.emission)
            self.nameDetailLayout.addWidget(labelDetail)

        self.established = False


        self.show()
        #self.channel.start_consuming()

class Detector(Receiver,object):
    
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
        #toDet = cv2.cvtColor(toDetect, cv2.COLOR_BGR2GRAY)
        #t = toDet.copy()
        
        #hornRect = self.lbpCascade.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #wakizashi0 = self.wakizashi.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #bastardsword0 = self.bastardsword.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #doot0 = self.doot.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #fouram0 = self.fouram.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #longbl0 = self.longbl.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        #sword0 = self.sword.detectMultiScale(toDet, scaleFactor = 1.2, minNeighbors = 5)
        clay0 = self.libpClay.detectMultiScale(toDetect, scaleFactor = 1.2, minNeighbors = 5)
        
        for (x, y, w, h) in clay0:
            #if (x <= 239):
            print("Found {0} hands!".format(len(clay0)))
            #self.count += 5*len(clay0)
            #if self.count >= 5:
            cv2.rectangle(toDetect, (x, y), (x+w, y+h), (10, 10, 200), 10)
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
        return toDetect

    def haar(self, img):
        toDetect = img.copy()
        
        hornRect = self.lbpCascade.detectMultiScale(toDetect, scaleFactor = 1.2, minNeighbors = 25)
        
        for (x, y, w, h) in hornRect:
            cv2.rectangle(toDetect, (x, y), (x+w, y+h), (10, 200, 10), 10)
            
        return toDetect

    


if __name__ == "__main__":
    #if len(sys.argv) != 4 :
    #    print("Usage is python main.py <username> <password> <url of rabbitmq server>")
    #    sys.exit()

    img = cv.imread('../computer-vision/pp/combinedPositives1/115img.jpg',0)
    
    
    vido = cv2.VideoCapture(0)
    appengine = QApplication([])
    
    det = Detector()
    

    #    sel.show()
            #Get the video frame
    try:
        ret, frame = vido.read()
    except e:
        print(e)
        #e as NoneType
    #detect using lbp
    toUseLBP = frame.copy()
    
    det = Detector()
    
    recv = Receiver()

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
    edges = cv.Canny(toUseLBP, recv.xVal, 200)
    
    #plt.subplot(121),plt.imshow(img,cmap = 'gray')
    #plt.title('Original Image'),plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image' ), plt.xticks([]), plt.yticks([])

    cv2.imshow('lbp vs haar', im)
    

    
    #vary 100 and 200 somehow


    #import dector
    #vido = cv2.VideoCapture(0)
    #det = Detector()
    #p = Path('.')
    #[x for x in p.iterdir() if x.is_dir()]
    #l = list(p.glob('**/*.py'))
    
    #app = QApplication([])
    #slider = QSlider()
    
    inputb = InputBox()
    #threader = threading.Thread(target=recv)
    #threader.show()
    #threader.start()
    threadee = threading.Thread(target=recv.run)
    threadee.start()
    recv.show()
    
    print("doot")
    det.show()
    while(True):
        try:
            ret, frame = vido.read()
        except e:
            print(e)
            #e as NoneType
        #detect using lbp
        toUseLBP = frame.copy()
        #im = det.lbp(toUseLBP)
        #toDet = cv2.cvtColor(toUseLBP, cv2.COLOR_BGR2GRAY)
        #toCanny = toDet.copy()
        #toCanny = im.copy()
        edges = cv.Canny(toUseLBP, recv.x, 200)
        print(str(recv.x))
        edgeDet = det.lbp(edges)
        #plt.subplot(121),plt.imshow(img,cmap = 'gray')
        #plt.title('Original Image'),plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(edges,cmap = 'gray')
        plt.title('Edge Image' ), plt.xticks([]), plt.yticks([])

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
        cv2.imshow('lbp vs haar', edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #vido.close()    
            vido.release()
            #cv2.destroyAllWindows()
            print("quitting...")
            break
    cv2.destroyAllWindows()
    #recv.appengine.exec()
    #app.exec()
    #app.destroy()
    #print(l)
    #while(True):
    #This is because app.exec() was just wrapped in sys.exit()
    #and I need to do some closing
    #
    #widget.connection.close()
    sys.exit()

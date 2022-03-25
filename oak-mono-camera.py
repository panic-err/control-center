#!/usr/bin/env python3

import cv2
import depthai as dai

import numpy as np
import pandas as pd

import sys

import threading

#maths
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from scipy import signal


import datetime


pipeline = dai.Pipeline()

monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
camRGB = pipeline.create(dai.node.ColorCamera)




#pipeline.setCameraTuningBlobPath('../computer-vision/mono-colourspace/tuning_mono_low_light.bin')


camoutRGB = pipeline.create(dai.node.XLinkOut)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutRight = pipeline.create(dai.node.XLinkOut)
controlIn = pipeline.create(dai.node.XLinkIn)
configIn = pipeline.create(dai.node.XLinkIn)

configMonoRIn = pipeline.create(dai.node.ImageManip)
manipROut = pipeline.create(dai.node.XLinkOut)
configMonoLIn = pipeline.create(dai.node.ImageManip)
manipLOut = pipeline.create(dai.node.XLinkOut)


configMonoRIn.initialConfig.setResize(300, 300)
configMonoRIn.initialConfig.setFrameType(dai.ImgFrame.Type.RAW8)
configMonoLIn.initialConfig.setResize(300, 300)
configMonoLIn.initialConfig.setFrameType(dai.ImgFrame.Type.RAW8)


xoutLeft.setStreamName('left')
xoutRight.setStreamName('right')
camoutRGB.setStreamName('rgb')
controlIn.setStreamName('control')
configIn.setStreamName('config')
manipROut.setStreamName('configuredR')
manipLOut.setStreamName('configuredL')




#topLeft = dai.Point2f(1, 1)
#bottomRight = dai.Point2f(1, 1)

topLeft = dai.Point2f(0.2, 0.2)
bottomRight = dai.Point2f(0.8, 0.8)


#mono camera
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)


configMonoRIn.initialConfig.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
configMonoLIn.initialConfig.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
configMonoRIn.setMaxOutputFrameSize(monoRight.getResolutionHeight()*monoRight.getResolutionWidth()*3)
configMonoLIn.setMaxOutputFrameSize(monoLeft.getResolutionHeight()*monoLeft.getResolutionWidth()*3)

#colur camera
camRGB.setBoardSocket(dai.CameraBoardSocket.RGB)
camRGB.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRGB.setVideoSize(300, 300)



camRGB.setPreviewSize(300, 300)
camRGB.setInterleaved(False)
camRGB.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

camRGB.still.link(camoutRGB.input)
camRGB.video.link(camoutRGB.input)


controlIn.out.link(camRGB.inputControl)

#monoLeft.out.link(xoutLeft.input)
#monoRight.out.link(xoutRight.input)
monoLeft.out.link(configMonoLIn.inputImage)
monoRight.out.link(configMonoRIn.inputImage)

#monoLeft.out.link(configMonoRIn.inputConfig)
#monoRight.out.link()


configIn.out.link(camRGB.inputConfig)
#configMonoRIn.out.link(configMonoRIn.inputConfig)
#configMonoRIn.out.link(monoRight.inputConfig)
#configMonoLIn.out.link(monoLeft.inputConfig)


def clamp(num, v0, v1):
    return max(v0, min(num, v1))





class IRConfig(threading.Thread):
    STEP_SIZE = 8
    EXP_STEP = 500
    ISO_STEP = 50
    LENS_STEP = 3
    WB_STEP = 200
    
    holdLeft = None
    holdRight = None
    def run(self):

        #It takes a while to do this step
        with dai.Device(pipeline) as device:
            # Defaults and limits for manual focus/exposure controls
            lensPos = 150
            lensMin = 0
            lensMax = 255

            expTime = 20000
            expMin = 1
            expMax = 33000

            sensIso = 800
            sensMin = 100
            sensMax = 1600
            
            wbManual = 4000
            wbMin = 1000
            wbMax = 12000


            #cmd = dai.RawCameraControl.Command(dai.RawCameraControl.Command.START_STREAM)

            #solar = dai.RawCameraControl.Command(dai.RawCameraControl.Command.EFFECT_MODE)
            
            #awb = dai.RawCameraControl.AutoWhiteBalanceMode(dai.RawCameraControl.AutoWhiteBalanceMode.OFF)
            #solar = solar.EffectMode.SOLARIZE
            
            
            #cme.EFFECT_MODE = cmd.EffectMode.SOLARIZE
            #still = dai.RawCameraControl.Command(dai.RawCameraControl.Command.STILL_CAPTURE)
            
            #end = dai.RawCameraControl.Command(dai.RawCameraControl.Command.STOP_STREAM)

            #cmd.STILL_CAPTURE
            #cmd.STOP_STREAM


            qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
            qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
            
            qRGB = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            qcontrol = device.getInputQueue(name="control", maxSize=4, blocking=False)
            
            
            count = 0
            ti = datetime.datetime.now()  
            tprevious = datetime.datetime.now()
            measurement = 0.
            BOTHFRAMES = False
            THISCYCLE = False
            
            countMonoDropped = 0
            countColorDropped = 0
            
            while True:
                 #print("Running the loop")
                
                try:
                    if self.holdLeft is None:
                        inLeft = qLeft.tryGet()
                    if self.holdRight is None:
                        inRight = qRight.tryGet()
                except Exception as e:
                    print("mono exception")
                    countMonoDropped += 1
                
               
                try:
                    inRGB = qRGB.tryGet()
                except Exception as e:
                    print("Color exception")
                    countColorDropped += 1
                
                
                if inLeft is not None:
                    self.holdLeft = inLeft
                if inRight is not None:
                    self.holdRight = inRight
                #Change the if condition to re-enable this block
                if inRGB is not None:
                    cv2.imshow('color', inRGB.getCvFrame())
                if self.holdLeft is not None and self.holdRight is not None:

                    #frameLeft = holdLeft.getCvFrame()
                    #frameRight = holdRight.getCvFrame()

                    BOTHFRAMES = True
                    THISCYCLE = True
                    #cv2.imshow("monoforall", holdLeft.getCvFrame())
                    #print(inRight)
                    #cv2.imshow("Right", holdRight.getCvFrame())

                key = cv2.waitKey(1)
                
                
                
                if THISCYCLE and BOTHFRAMES and key == ord('z'):
                    
                    #frameLeft = holdLeft.getCvFrame()
                    #frameRight = holdRight.getCvFrame()
                    print(self.holdLeft)
                    print(type(self.holdLeft))
                    print(self.holdLeft.getType())
                    rawFrameLeft = self.holdLeft.getRaw()
                    print(rawFrameLeft)
                    print("Type of raw frame left" + str(type(rawFrameLeft)))
                    print(self.holdRight)
                    print(type(self.holdRight))
                    holdLeft = None
                    holdRight = None
                    BOTHFRAMES = False
                elif key == ord('z') and self.holdLeft is not None:
                    print("Left frame: "+str(self.holdLeft))
                    print("Left type: "+str(type(self.holdLeft)))
                    rawFrameLeft = self.holdLeft.getRaw()
                    print(rawFrameLeft)
                    print("Type of raw frame left" + str(type(rawFrameLeft)))
                elif key == ord('p'):
                    print("Taking picture")
                    ctrl = dai.CameraControl()
                    ctrl.setCaptureStill(True)
                    qcontrol.send(ctrl)
                    key = None
                elif key in [ord('3'), ord('4')]:
                    if key == ord('3'):
                        expTime = 500
                        print("Setting manual exposure to ",str(expTime))
                        
                    if key == ord('4'): 
                        sensIso = 1600
                        print("Setting ISO to ",str(sensIso))
                    expTime = clamp(expTime, expMin, expMax)
                    sensIso = clamp(sensIso, sensMin, sensMax)
                    ctrl = dai.CameraControl()
                    ctrl.setManualExposure(expTime, sensIso)
                    qcontrol.send(ctrl)
                elif key in [ord('i'), ord('o'), ord('k'), ord('l')]:
                    if key == ord('i'): expTime -= self.EXP_STEP
                    if key == ord('o'): expTime += self.EXP_STEP
                    if key == ord('k'): sensIso -= self.ISO_STEP
                    if key == ord('l'): sensIso += self.ISO_STEP
                    expTime = clamp(expTime, expMin, expMax)
                    sensIso = clamp(sensIso, sensMin, sensMax)
                    print("Setting manual exposure time: ", expTime, "iso: ", sensIso)
                    ctrl = dai.CameraControl()
                    ctrl.setManualExposure(expTime, sensIso)
                    qcontrol.send(ctrl)
                #holdLeft = None
                #holdRight = None
                THISCYCLE = False    
                if key == ord('q'):
                    
                    break
        sys.exit()

if __name__ == "__main__":
    print("Making this a multi-threaded application")
    t = IRConfig()
    
    t = threading.Thread(target=t.run)
    t.start()
    

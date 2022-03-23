#!/usr/bin/env python3

import cv2
import depthai as dai

import numpy as np
import pandas as pd

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


xoutLeft.setStreamName('left')
xoutRight.setStreamName('right')
camoutRGB.setStreamName('rgb')
controlIn.setStreamName('control')
configIn.setStreamName('config')

monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
camRGB.setBoardSocket(dai.CameraBoardSocket.RGB)
camRGB.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
#camRGB.setVideoSize(1920, 1080)


#camRGB.setPreviewSize(300, 300)
camRGB.setInterleaved(False)
camRGB.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

camRGB.still.link(camoutRGB.input)
controlIn.out.link(camRGB.inputControl)

monoLeft.out.link(xoutLeft.input)
monoRight.out.link(xoutRight.input)

configIn.out.link(camRGB.inputConfig)

STEP_SIZE = 8
EXP_STEP = 500
ISO_STEP = 50
LENS_STEP = 3
WB_STEP = 200

def clamp(num, v0, v1):
    return max(v0, min(num, v1))

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
    t = datetime.datetime.now()  
    tprevious = datetime.datetime.now()
    measurement = 0.
    holdLeft = None
    holdRight = None
    while True:

        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()
        
        inRGB = qRGB.tryGet()
        
        
        
        if inLeft is not None:
            holdLeft = inLeft
        if inRight is not None:
            holdRight = inRight
        if inRGB is not None:
            data = inRGB.getData()
            print(str(data))
            print(str(type(data)))
            print(str(data.shape))
            shape = (3110400,)
            
            dataBlobZeros = np.empty(shape, dtype=np.float64, order='C')
            dataArray = np.array(data, dtype=np.float64, order='C')
            
            
            dataBlob = pd.DataFrame(dataArray)
            #find columns of type int
            mask = dataBlob.dtypes==np.float64
            #select columns for the same
            cols = dataBlob.dtypes[mask].index
            #select these columns and convert to float
            dataBlobNew = dataBlob[cols].apply(lambda x: x.multiply(x, x))
            dataBlob[dataBlobNew.columns] = dataBlobNew
            print(str(dataBlob))
            print(str(type(dataBlob)))
            
            #a = np.zeros(shape, dtype=float, order='C')
            #print(str(a))
            #print(str(type(a)))
            #a = np.multiply(data, data)
            #print(str(a))
            #print(str(a.shape))
        if holdLeft is not None and holdRight is not None:
            count += 1
            #print(inLeft)
            t2 = datetime.datetime.now()
            
            #hold = holdLeft * holdRight
            #print(str(holdLeft.getData())+"Type")
            
            c = t2 - t
            tprevious = c
            smoothing = 0.9
            measurement = (measurement * smoothing) + (tprevious.total_seconds() * (1.0-smoothing))
            #print("Time for both frames is : " + str(c.total_seconds()*1000))
            
            fps = 1/(measurement)
            #print("FPS is " + str(fps))
            t = datetime.datetime.now()
            cv2.imshow("monoforall", holdLeft.getCvFrame())
            #print(inRight)
            cv2.imshow("Right", holdRight.getCvFrame())
            holdLeft = None
            holdRight = None
    
        key = cv2.waitKey(1)
        
        if key == ord('p'):
            print("Taking picture")
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qcontrol.send(ctrl)
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
            if key == ord('i'): expTime -= EXP_STEP
            if key == ord('o'): expTime += EXP_STEP
            if key == ord('k'): sensIso -= ISO_STEP
            if key == ord('l'): sensIso += ISO_STEP
            expTime = clamp(expTime, expMin, expMax)
            sensIso = clamp(sensIso, sensMin, sensMax)
            print("Setting manual exposure time: ", expTime, "iso: ", sensIso)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(expTime, sensIso)
            qcontrol.send(ctrl)
        if key == ord('q'):
            
            break


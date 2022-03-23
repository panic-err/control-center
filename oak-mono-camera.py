#!/usr/bin/env python3

import cv2
import depthai as dai

import datetime


pipeline = dai.Pipeline()

monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)

pipeline.setCameraTuningBlobPath('../computer-vision/mono-colourspace/tuning_mono_low_light.bin')



xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutRight = pipeline.create(dai.node.XLinkOut)


xoutLeft.setStreamName('left')
xoutRight.setStreamName('right')

monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)

monoLeft.out.link(xoutLeft.input)
monoRight.out.link(xoutRight.input)


#It takes a while to do this step
with dai.Device(pipeline) as device:


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
    count = 0
    t = datetime.datetime.now()  
    tprevious = datetime.datetime.now()
    measurement = 0.
    holdLeft = None
    holdRight = None
    while True:

        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()
        
        if inLeft is not None:
            holdLeft = inLeft
        if inRight is not None:
            holdRight = inRight
        
        
        if holdLeft is not None and  holdRight is not None:
            count += 1
            print(inLeft)
            t2 = datetime.datetime.now()
            
            c = t2 - t
            tprevious = c
            smoothing = 0.9
            measurement = (measurement * smoothing) + (tprevious.total_seconds() * (1.0-smoothing))
            print("Time for both frames is : " + str(c.total_seconds()*1000))
            
            fps = 1/(measurement)
            print("FPS is " + str(fps))
            t = datetime.datetime.now()
            cv2.imshow("monoforall", holdLeft.getCvFrame())
            print(inRight)
            cv2.imshow("Right", holdRight.getCvFrame())
            holdLeft = None
            holdRight = None
    
        if cv2.waitKey(1) == ord('q'):
            
            break


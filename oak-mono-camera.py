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
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

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
    
    while True:
        t = datetime.datetime.now()
        inLeft = qLeft.tryGet()
        inRight = qRight.tryGet()
        
        if inLeft is not None and inRight is not None:
            print(inLeft)
            t2 = datetime.datetime.now()
            c = t - t2
            print("Time is : " + str(c.total_seconds()*1000))
            cv2.imshow("monoforall", inLeft.getCvFrame())
            print(inRight)
            cv2.imshow("Right", inRight.getCvFrame())
        
        if cv2.waitKey(1) == ord('q'):
            
            break

